---
skill: cli-tool-patterns
version: 1.0.0
used-by:
  - utility-builder
  - script-builder
---

# CLI Tool Development Patterns

Production-ready patterns for building command-line tools with TypeScript.

## 1. Project Setup

### Directory Structure

```
my-cli/
├── src/
│   ├── index.ts           # Entry point with shebang
│   ├── cli.ts             # CLI definition
│   ├── commands/          # Command implementations
│   │   ├── init.ts
│   │   ├── build.ts
│   │   └── deploy.ts
│   ├── lib/               # Core logic
│   │   ├── config.ts
│   │   ├── errors.ts
│   │   └── utils.ts
│   ├── prompts/           # Interactive prompts
│   │   └── setup.ts
│   └── types/             # Type definitions
│       └── index.ts
├── templates/             # Template files for scaffolding
├── package.json
├── tsconfig.json
└── vitest.config.ts
```

### package.json Configuration

```json
{
  "name": "my-cli",
  "version": "1.0.0",
  "description": "A production CLI tool",
  "type": "module",
  "bin": {
    "my-cli": "./dist/index.js"
  },
  "files": [
    "dist",
    "templates"
  ],
  "scripts": {
    "build": "tsup src/index.ts --format esm --dts --clean",
    "dev": "tsup src/index.ts --format esm --watch",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "test:watch": "vitest",
    "prepublishOnly": "npm run build"
  },
  "dependencies": {
    "chalk": "^5.3.0",
    "commander": "^12.0.0",
    "cosmiconfig": "^9.0.0",
    "ora": "^8.0.0",
    "prompts": "^2.4.2"
  },
  "devDependencies": {
    "@types/node": "^20.11.0",
    "@types/prompts": "^2.4.9",
    "tsup": "^8.0.0",
    "typescript": "^5.3.0",
    "vitest": "^1.2.0"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "lib": ["ES2022"],
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "declaration": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Entry Point with Shebang

```typescript
#!/usr/bin/env node
// src/index.ts

import { cli } from './cli.js';

cli.parse(process.argv);
```

## 2. Commander.js Patterns

### Basic CLI Setup

```typescript
// src/cli.ts
import { Command } from 'commander';
import { version } from '../package.json' assert { type: 'json' };
import { initCommand } from './commands/init.js';
import { buildCommand } from './commands/build.js';
import { deployCommand } from './commands/deploy.js';

export const cli = new Command()
  .name('my-cli')
  .description('A production CLI tool for project management')
  .version(version, '-v, --version', 'Display version number')
  .option('-d, --debug', 'Enable debug output', false)
  .option('-c, --config <path>', 'Path to config file')
  .hook('preAction', (thisCommand) => {
    const options = thisCommand.opts();
    if (options.debug) {
      process.env.DEBUG = 'true';
    }
  });

// Register commands
cli.addCommand(initCommand);
cli.addCommand(buildCommand);
cli.addCommand(deployCommand);

// Default action when no command specified
cli.action(() => {
  cli.help();
});
```

### Command with Options and Arguments

```typescript
// src/commands/init.ts
import { Command } from 'commander';
import chalk from 'chalk';
import { CLIError } from '../lib/errors.js';
import { runInitPrompts } from '../prompts/setup.js';
import { createProject } from '../lib/project.js';

export const initCommand = new Command('init')
  .description('Initialize a new project')
  .argument('[name]', 'Project name')
  .option('-t, --template <template>', 'Template to use', 'default')
  .option('--typescript', 'Use TypeScript', true)
  .option('--no-typescript', 'Use JavaScript')
  .option('--git', 'Initialize git repository', true)
  .option('--no-git', 'Skip git initialization')
  .option('-p, --package-manager <pm>', 'Package manager', 'npm')
  .option('--dry-run', 'Show what would be created without writing files')
  .action(async (name, options) => {
    try {
      // Run interactive prompts if name not provided
      const config = name
        ? { name, ...options }
        : await runInitPrompts(options);

      if (options.dryRun) {
        console.log(chalk.yellow('Dry run - no files will be created'));
        console.log(chalk.dim(JSON.stringify(config, null, 2)));
        return;
      }

      await createProject(config);
      console.log(chalk.green(`Project ${config.name} created successfully!`));
    } catch (error) {
      if (error instanceof CLIError) {
        console.error(chalk.red(`Error: ${error.message}`));
        process.exit(error.exitCode);
      }
      throw error;
    }
  });
```

### Subcommands Pattern

```typescript
// src/commands/deploy.ts
import { Command } from 'commander';
import chalk from 'chalk';
import ora from 'ora';

export const deployCommand = new Command('deploy')
  .description('Deploy your project');

// Subcommand: deploy preview
deployCommand
  .command('preview')
  .description('Deploy to preview environment')
  .option('--branch <branch>', 'Branch to deploy')
  .action(async (options) => {
    const spinner = ora('Deploying to preview...').start();
    try {
      // Deploy logic here
      await deployToPreview(options);
      spinner.succeed('Deployed to preview');
    } catch (error) {
      spinner.fail('Deployment failed');
      throw error;
    }
  });

// Subcommand: deploy production
deployCommand
  .command('production')
  .alias('prod')
  .description('Deploy to production')
  .option('--skip-tests', 'Skip test suite')
  .option('--force', 'Force deployment without confirmation')
  .action(async (options) => {
    if (!options.force) {
      const confirmed = await confirmProduction();
      if (!confirmed) {
        console.log(chalk.yellow('Deployment cancelled'));
        return;
      }
    }
    await deployToProduction(options);
  });

// Subcommand: deploy rollback
deployCommand
  .command('rollback')
  .description('Rollback to previous deployment')
  .argument('<version>', 'Version to rollback to')
  .action(async (version) => {
    await rollbackDeployment(version);
  });
```

### Command with Variadic Arguments

```typescript
// src/commands/build.ts
import { Command } from 'commander';

export const buildCommand = new Command('build')
  .description('Build project files')
  .argument('[files...]', 'Files to build (default: all)')
  .option('-o, --output <dir>', 'Output directory', 'dist')
  .option('-w, --watch', 'Watch for changes')
  .option('--minify', 'Minify output')
  .option('--sourcemap', 'Generate sourcemaps')
  .action(async (files, options) => {
    const filesToBuild = files.length > 0 ? files : await getAllFiles();
    await buildFiles(filesToBuild, options);
  });
```

## 3. Interactive Prompts

### Using prompts Library

```typescript
// src/prompts/setup.ts
import prompts from 'prompts';
import chalk from 'chalk';
import { CLIError } from '../lib/errors.js';

interface InitConfig {
  name: string;
  template: string;
  typescript: boolean;
  git: boolean;
  packageManager: 'npm' | 'yarn' | 'pnpm';
  features: string[];
}

export async function runInitPrompts(
  defaults: Partial<InitConfig> = {}
): Promise<InitConfig> {
  // Handle Ctrl+C gracefully
  prompts.override(defaults);

  const onCancel = () => {
    throw new CLIError('Setup cancelled', 130);
  };

  const response = await prompts(
    [
      {
        type: 'text',
        name: 'name',
        message: 'Project name:',
        initial: defaults.name || 'my-project',
        validate: (value) => {
          if (!value) return 'Project name is required';
          if (!/^[a-z0-9-_]+$/i.test(value)) {
            return 'Name can only contain letters, numbers, dashes, and underscores';
          }
          return true;
        },
      },
      {
        type: 'select',
        name: 'template',
        message: 'Select a template:',
        choices: [
          { title: 'Default', value: 'default', description: 'Basic starter template' },
          { title: 'API', value: 'api', description: 'REST API with Express' },
          { title: 'Full Stack', value: 'fullstack', description: 'Next.js with API routes' },
          { title: 'Library', value: 'library', description: 'NPM package template' },
        ],
        initial: 0,
      },
      {
        type: 'toggle',
        name: 'typescript',
        message: 'Use TypeScript?',
        initial: defaults.typescript ?? true,
        active: 'yes',
        inactive: 'no',
      },
      {
        type: 'select',
        name: 'packageManager',
        message: 'Package manager:',
        choices: [
          { title: 'npm', value: 'npm' },
          { title: 'yarn', value: 'yarn' },
          { title: 'pnpm', value: 'pnpm' },
        ],
        initial: 0,
      },
      {
        type: 'multiselect',
        name: 'features',
        message: 'Select features:',
        choices: [
          { title: 'ESLint', value: 'eslint', selected: true },
          { title: 'Prettier', value: 'prettier', selected: true },
          { title: 'Husky (git hooks)', value: 'husky' },
          { title: 'GitHub Actions', value: 'github-actions' },
          { title: 'Docker', value: 'docker' },
        ],
        hint: '- Space to select. Return to submit',
      },
      {
        type: 'toggle',
        name: 'git',
        message: 'Initialize git repository?',
        initial: defaults.git ?? true,
        active: 'yes',
        inactive: 'no',
      },
    ],
    { onCancel }
  );

  return response as InitConfig;
}
```

### Confirmation Prompts

```typescript
// src/prompts/confirm.ts
import prompts from 'prompts';
import chalk from 'chalk';

export async function confirmAction(
  message: string,
  initial = false
): Promise<boolean> {
  const { confirmed } = await prompts({
    type: 'confirm',
    name: 'confirmed',
    message,
    initial,
  });
  return confirmed ?? false;
}

export async function confirmDangerous(action: string): Promise<boolean> {
  console.log(chalk.red.bold('\nWarning: This action cannot be undone!'));

  const { typedConfirm } = await prompts({
    type: 'text',
    name: 'typedConfirm',
    message: `Type "${action}" to confirm:`,
    validate: (value) =>
      value === action ? true : `Please type "${action}" exactly`,
  });

  return typedConfirm === action;
}

export async function selectFromList<T>(
  message: string,
  items: Array<{ title: string; value: T; description?: string }>
): Promise<T | undefined> {
  const { selected } = await prompts({
    type: 'select',
    name: 'selected',
    message,
    choices: items,
  });
  return selected;
}
```

### Password and Sensitive Input

```typescript
// src/prompts/auth.ts
import prompts from 'prompts';

export async function getCredentials(): Promise<{
  username: string;
  password: string;
} | null> {
  const response = await prompts([
    {
      type: 'text',
      name: 'username',
      message: 'Username:',
      validate: (value) => (value ? true : 'Username required'),
    },
    {
      type: 'password',
      name: 'password',
      message: 'Password:',
      validate: (value) =>
        value.length >= 8 ? true : 'Password must be at least 8 characters',
    },
  ]);

  if (!response.username || !response.password) {
    return null;
  }

  return response;
}

export async function getApiKey(): Promise<string | null> {
  const { apiKey } = await prompts({
    type: 'password',
    name: 'apiKey',
    message: 'Enter your API key:',
    validate: (value) => {
      if (!value) return 'API key is required';
      if (!/^[a-zA-Z0-9_-]{32,}$/.test(value)) {
        return 'Invalid API key format';
      }
      return true;
    },
  });
  return apiKey || null;
}
```

## 4. Output and Feedback

### Chalk for Colored Output

```typescript
// src/lib/logger.ts
import chalk from 'chalk';

export const logger = {
  info: (message: string) => {
    console.log(chalk.blue('info') + ' ' + message);
  },

  success: (message: string) => {
    console.log(chalk.green('success') + ' ' + message);
  },

  warn: (message: string) => {
    console.log(chalk.yellow('warn') + ' ' + message);
  },

  error: (message: string) => {
    console.error(chalk.red('error') + ' ' + message);
  },

  debug: (message: string) => {
    if (process.env.DEBUG) {
      console.log(chalk.gray('debug') + ' ' + chalk.dim(message));
    }
  },

  // Styled output helpers
  highlight: (text: string) => chalk.cyan(text),
  dim: (text: string) => chalk.dim(text),
  bold: (text: string) => chalk.bold(text),
  code: (text: string) => chalk.bgGray.white(` ${text} `),

  // Multi-line box output
  box: (title: string, content: string) => {
    const width = 60;
    const line = chalk.gray('─'.repeat(width));
    console.log(line);
    console.log(chalk.bold(title));
    console.log(line);
    console.log(content);
    console.log(line);
  },

  // List output
  list: (items: string[], bullet = '•') => {
    items.forEach((item) => {
      console.log(chalk.gray(bullet) + ' ' + item);
    });
  },

  // Key-value pairs
  keyValue: (pairs: Record<string, string>) => {
    const maxKeyLength = Math.max(...Object.keys(pairs).map((k) => k.length));
    Object.entries(pairs).forEach(([key, value]) => {
      console.log(
        chalk.gray(key.padEnd(maxKeyLength)) + '  ' + chalk.white(value)
      );
    });
  },
};
```

### Ora Spinners

```typescript
// src/lib/spinner.ts
import ora, { Ora } from 'ora';

export function createSpinner(text: string): Ora {
  return ora({
    text,
    color: 'cyan',
    spinner: 'dots',
  });
}

export async function withSpinner<T>(
  text: string,
  task: () => Promise<T>,
  options: {
    successText?: string;
    failText?: string;
  } = {}
): Promise<T> {
  const spinner = createSpinner(text).start();

  try {
    const result = await task();
    spinner.succeed(options.successText || text);
    return result;
  } catch (error) {
    spinner.fail(options.failText || text);
    throw error;
  }
}

// Sequential tasks with spinners
export async function runTasks(
  tasks: Array<{
    text: string;
    task: () => Promise<void>;
  }>
): Promise<void> {
  for (const { text, task } of tasks) {
    await withSpinner(text, task);
  }
}

// Example usage
export async function installDependencies(): Promise<void> {
  await runTasks([
    {
      text: 'Installing dependencies',
      task: async () => {
        await execAsync('npm install');
      },
    },
    {
      text: 'Building project',
      task: async () => {
        await execAsync('npm run build');
      },
    },
    {
      text: 'Running tests',
      task: async () => {
        await execAsync('npm test');
      },
    },
  ]);
}
```

### Progress Bars

```typescript
// src/lib/progress.ts
import chalk from 'chalk';

interface ProgressBarOptions {
  total: number;
  width?: number;
  complete?: string;
  incomplete?: string;
  format?: string;
}

export class ProgressBar {
  private current = 0;
  private total: number;
  private width: number;
  private complete: string;
  private incomplete: string;

  constructor(options: ProgressBarOptions) {
    this.total = options.total;
    this.width = options.width || 40;
    this.complete = options.complete || '█';
    this.incomplete = options.incomplete || '░';
  }

  update(current: number, message?: string): void {
    this.current = current;
    const percent = Math.min(100, Math.floor((current / this.total) * 100));
    const filledWidth = Math.floor((current / this.total) * this.width);
    const emptyWidth = this.width - filledWidth;

    const bar =
      chalk.green(this.complete.repeat(filledWidth)) +
      chalk.gray(this.incomplete.repeat(emptyWidth));

    const status = `${current}/${this.total}`;
    const line = `${bar} ${percent}% ${status}${message ? ` - ${message}` : ''}`;

    process.stdout.clearLine(0);
    process.stdout.cursorTo(0);
    process.stdout.write(line);
  }

  complete(): void {
    this.update(this.total);
    console.log(); // New line after completion
  }
}

// Usage example
export async function processFiles(files: string[]): Promise<void> {
  const progress = new ProgressBar({ total: files.length });

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    await processFile(file);
    progress.update(i + 1, file);
  }

  progress.complete();
}
```

### Table Output

```typescript
// src/lib/table.ts
import chalk from 'chalk';

interface TableColumn {
  key: string;
  header: string;
  width?: number;
  align?: 'left' | 'right' | 'center';
}

export function printTable(
  data: Record<string, string | number>[],
  columns: TableColumn[]
): void {
  // Calculate column widths
  const widths = columns.map((col) => {
    const maxData = Math.max(
      ...data.map((row) => String(row[col.key] || '').length)
    );
    return col.width || Math.max(col.header.length, maxData);
  });

  // Print header
  const headerLine = columns
    .map((col, i) => chalk.bold(col.header.padEnd(widths[i])))
    .join('  ');
  console.log(headerLine);
  console.log(chalk.gray('─'.repeat(headerLine.length)));

  // Print rows
  data.forEach((row) => {
    const line = columns
      .map((col, i) => {
        const value = String(row[col.key] || '');
        const width = widths[i];
        switch (col.align) {
          case 'right':
            return value.padStart(width);
          case 'center':
            const pad = Math.floor((width - value.length) / 2);
            return ' '.repeat(pad) + value + ' '.repeat(width - pad - value.length);
          default:
            return value.padEnd(width);
        }
      })
      .join('  ');
    console.log(line);
  });
}

// Usage
printTable(
  [
    { name: 'package.json', size: 1024, modified: '2024-01-15' },
    { name: 'tsconfig.json', size: 512, modified: '2024-01-14' },
  ],
  [
    { key: 'name', header: 'File', width: 20 },
    { key: 'size', header: 'Size', width: 10, align: 'right' },
    { key: 'modified', header: 'Modified', width: 12 },
  ]
);
```

## 5. File Operations

### Safe File Writing

```typescript
// src/lib/files.ts
import { mkdir, writeFile, readFile, access, rm } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { constants } from 'node:fs';
import chalk from 'chalk';
import { CLIError } from './errors.js';

export async function fileExists(path: string): Promise<boolean> {
  try {
    await access(path, constants.F_OK);
    return true;
  } catch {
    return false;
  }
}

export async function ensureDir(dirPath: string): Promise<void> {
  await mkdir(dirPath, { recursive: true });
}

export async function safeWriteFile(
  filePath: string,
  content: string,
  options: {
    overwrite?: boolean;
    createDir?: boolean;
    dryRun?: boolean;
  } = {}
): Promise<void> {
  const { overwrite = false, createDir = true, dryRun = false } = options;
  const absolutePath = resolve(filePath);

  // Check if file exists
  if (!overwrite && (await fileExists(absolutePath))) {
    throw new CLIError(
      `File already exists: ${filePath}. Use --overwrite to replace.`,
      1
    );
  }

  if (dryRun) {
    console.log(chalk.dim(`Would write: ${absolutePath}`));
    return;
  }

  // Create directory if needed
  if (createDir) {
    await ensureDir(dirname(absolutePath));
  }

  await writeFile(absolutePath, content, 'utf-8');
}

export async function writeFiles(
  files: Array<{ path: string; content: string }>,
  options: { baseDir?: string; dryRun?: boolean; overwrite?: boolean } = {}
): Promise<string[]> {
  const { baseDir = process.cwd(), dryRun = false, overwrite = false } = options;
  const written: string[] = [];

  for (const file of files) {
    const fullPath = join(baseDir, file.path);
    await safeWriteFile(fullPath, file.content, { dryRun, overwrite });
    written.push(fullPath);

    if (!dryRun) {
      console.log(chalk.green('  created') + ' ' + file.path);
    }
  }

  return written;
}

export async function copyTemplate(
  templatePath: string,
  destPath: string,
  variables: Record<string, string>
): Promise<void> {
  let content = await readFile(templatePath, 'utf-8');

  // Replace template variables: {{variableName}}
  for (const [key, value] of Object.entries(variables)) {
    content = content.replace(new RegExp(`\\{\\{${key}\\}\\}`, 'g'), value);
  }

  await safeWriteFile(destPath, content, { createDir: true });
}
```

### Template Processing

```typescript
// src/lib/templates.ts
import { readFile, readdir } from 'node:fs/promises';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));

export interface TemplateFile {
  path: string;
  content: string;
}

export async function loadTemplate(
  templateName: string,
  variables: Record<string, string> = {}
): Promise<TemplateFile[]> {
  const templateDir = join(__dirname, '../../templates', templateName);
  return processTemplateDir(templateDir, templateDir, variables);
}

async function processTemplateDir(
  dir: string,
  baseDir: string,
  variables: Record<string, string>
): Promise<TemplateFile[]> {
  const files: TemplateFile[] = [];
  const entries = await readdir(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = join(dir, entry.name);
    const relativePath = relative(baseDir, fullPath);

    if (entry.isDirectory()) {
      const subFiles = await processTemplateDir(fullPath, baseDir, variables);
      files.push(...subFiles);
    } else {
      let content = await readFile(fullPath, 'utf-8');

      // Process template variables
      content = processTemplateContent(content, variables);

      // Process filename variables
      const processedPath = processTemplateContent(relativePath, variables);

      files.push({ path: processedPath, content });
    }
  }

  return files;
}

function processTemplateContent(
  content: string,
  variables: Record<string, string>
): string {
  // Replace {{variable}} syntax
  return content.replace(/\{\{(\w+)\}\}/g, (match, key) => {
    return variables[key] ?? match;
  });
}

// Conditional template blocks
export function processConditionals(
  content: string,
  conditions: Record<string, boolean>
): string {
  // Process {{#if condition}}...{{/if}} blocks
  return content.replace(
    /\{\{#if (\w+)\}\}([\s\S]*?)\{\{\/if\}\}/g,
    (match, condition, block) => {
      return conditions[condition] ? block : '';
    }
  );
}
```

## 6. Error Handling

### Custom CLI Error Class

```typescript
// src/lib/errors.ts
import chalk from 'chalk';

export class CLIError extends Error {
  constructor(
    message: string,
    public exitCode: number = 1,
    public details?: string
  ) {
    super(message);
    this.name = 'CLIError';
  }

  static validation(field: string, expected: string): CLIError {
    return new CLIError(
      `Invalid ${field}: expected ${expected}`,
      1
    );
  }

  static fileNotFound(path: string): CLIError {
    return new CLIError(`File not found: ${path}`, 1);
  }

  static configNotFound(): CLIError {
    return new CLIError(
      'No configuration file found. Run "my-cli init" first.',
      1
    );
  }

  static networkError(url: string, statusCode?: number): CLIError {
    const details = statusCode ? ` (status: ${statusCode})` : '';
    return new CLIError(`Network request failed: ${url}${details}`, 1);
  }

  static permissionDenied(path: string): CLIError {
    return new CLIError(`Permission denied: ${path}`, 1);
  }

  static cancelled(): CLIError {
    return new CLIError('Operation cancelled', 130);
  }
}

export function formatError(error: unknown): string {
  if (error instanceof CLIError) {
    let message = chalk.red('Error: ') + error.message;
    if (error.details) {
      message += '\n' + chalk.dim(error.details);
    }
    return message;
  }

  if (error instanceof Error) {
    return chalk.red('Error: ') + error.message;
  }

  return chalk.red('Error: ') + String(error);
}

export function handleError(error: unknown): never {
  console.error(formatError(error));

  if (process.env.DEBUG && error instanceof Error && error.stack) {
    console.error(chalk.dim(error.stack));
  }

  const exitCode = error instanceof CLIError ? error.exitCode : 1;
  process.exit(exitCode);
}
```

### Global Error Handler

```typescript
// src/index.ts
#!/usr/bin/env node

import { cli } from './cli.js';
import { handleError, CLIError } from './lib/errors.js';

// Handle unhandled rejections
process.on('unhandledRejection', (reason) => {
  handleError(reason);
});

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  handleError(error);
});

// Handle SIGINT (Ctrl+C)
process.on('SIGINT', () => {
  console.log('\n');
  handleError(CLIError.cancelled());
});

// Run CLI
try {
  await cli.parseAsync(process.argv);
} catch (error) {
  handleError(error);
}
```

### Async Error Wrapper

```typescript
// src/lib/utils.ts
import { CLIError } from './errors.js';

export function wrapCommand<T extends (...args: unknown[]) => Promise<void>>(
  fn: T
): T {
  return (async (...args: Parameters<T>) => {
    try {
      await fn(...args);
    } catch (error) {
      if (error instanceof CLIError) {
        throw error;
      }

      // Convert common errors to CLIError
      if (error instanceof Error) {
        if (error.message.includes('ENOENT')) {
          throw CLIError.fileNotFound(error.message);
        }
        if (error.message.includes('EACCES')) {
          throw CLIError.permissionDenied(error.message);
        }
      }

      throw error;
    }
  }) as T;
}
```

## 7. Configuration Management

### Using cosmiconfig

```typescript
// src/lib/config.ts
import { cosmiconfig, cosmiconfigSync } from 'cosmiconfig';
import { z } from 'zod';
import { CLIError } from './errors.js';

// Define config schema with Zod
const ConfigSchema = z.object({
  name: z.string().optional(),
  version: z.string().default('1.0.0'),
  outDir: z.string().default('dist'),
  sourceDir: z.string().default('src'),
  typescript: z.boolean().default(true),
  features: z.object({
    minify: z.boolean().default(false),
    sourcemaps: z.boolean().default(true),
  }).default({}),
  deploy: z.object({
    provider: z.enum(['vercel', 'netlify', 'aws']).optional(),
    region: z.string().optional(),
  }).optional(),
});

export type Config = z.infer<typeof ConfigSchema>;

const explorer = cosmiconfig('mycli', {
  searchPlaces: [
    'package.json',
    'mycli.config.js',
    'mycli.config.mjs',
    'mycli.config.ts',
    '.myclirc',
    '.myclirc.json',
    '.myclirc.yaml',
    '.myclirc.yml',
  ],
});

let cachedConfig: Config | null = null;

export async function loadConfig(configPath?: string): Promise<Config> {
  if (cachedConfig) {
    return cachedConfig;
  }

  const result = configPath
    ? await explorer.load(configPath)
    : await explorer.search();

  if (!result || result.isEmpty) {
    throw CLIError.configNotFound();
  }

  // Validate config
  const parsed = ConfigSchema.safeParse(result.config);
  if (!parsed.success) {
    const errors = parsed.error.errors
      .map((e) => `  ${e.path.join('.')}: ${e.message}`)
      .join('\n');
    throw new CLIError(`Invalid configuration:\n${errors}`, 1);
  }

  cachedConfig = parsed.data;
  return cachedConfig;
}

export function loadConfigSync(configPath?: string): Config {
  if (cachedConfig) {
    return cachedConfig;
  }

  const explorerSync = cosmiconfigSync('mycli');
  const result = configPath
    ? explorerSync.load(configPath)
    : explorerSync.search();

  if (!result || result.isEmpty) {
    throw CLIError.configNotFound();
  }

  const parsed = ConfigSchema.safeParse(result.config);
  if (!parsed.success) {
    throw new CLIError('Invalid configuration', 1);
  }

  cachedConfig = parsed.data;
  return cachedConfig;
}

export function clearConfigCache(): void {
  cachedConfig = null;
}
```

### Config File Generator

```typescript
// src/lib/config-init.ts
import { writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import chalk from 'chalk';

export async function generateConfig(
  options: {
    format?: 'json' | 'js' | 'yaml';
    dir?: string;
  } = {}
): Promise<string> {
  const { format = 'json', dir = process.cwd() } = options;

  const config = {
    name: 'my-project',
    version: '1.0.0',
    outDir: 'dist',
    sourceDir: 'src',
    typescript: true,
    features: {
      minify: false,
      sourcemaps: true,
    },
  };

  let content: string;
  let filename: string;

  switch (format) {
    case 'js':
      filename = 'mycli.config.js';
      content = `/** @type {import('my-cli').Config} */
export default ${JSON.stringify(config, null, 2)};
`;
      break;

    case 'yaml':
      filename = '.myclirc.yaml';
      content = Object.entries(config)
        .map(([key, value]) => {
          if (typeof value === 'object') {
            const nested = Object.entries(value)
              .map(([k, v]) => `  ${k}: ${v}`)
              .join('\n');
            return `${key}:\n${nested}`;
          }
          return `${key}: ${value}`;
        })
        .join('\n');
      break;

    default:
      filename = '.myclirc.json';
      content = JSON.stringify(config, null, 2);
  }

  const filePath = join(dir, filename);
  await writeFile(filePath, content, 'utf-8');

  console.log(chalk.green('Created') + ' ' + filename);
  return filePath;
}
```

## 8. Testing CLIs

### Test Setup with Vitest

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['src/**/*.test.ts', 'tests/**/*.test.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      include: ['src/**/*.ts'],
      exclude: ['src/**/*.test.ts'],
    },
  },
});
```

### Testing Commands

```typescript
// tests/commands/init.test.ts
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { vol } from 'memfs';
import { initCommand } from '../../src/commands/init.js';

// Mock fs with memfs
vi.mock('node:fs/promises', async () => {
  const memfs = await import('memfs');
  return memfs.fs.promises;
});

describe('init command', () => {
  beforeEach(() => {
    vol.reset();
    vol.mkdirSync('/project', { recursive: true });
    process.chdir('/project');
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('creates project with default template', async () => {
    await initCommand.parseAsync(['node', 'test', 'my-app']);

    expect(vol.existsSync('/project/my-app/package.json')).toBe(true);
    expect(vol.existsSync('/project/my-app/src/index.ts')).toBe(true);
  });

  it('creates project with specified template', async () => {
    await initCommand.parseAsync([
      'node',
      'test',
      'my-api',
      '--template',
      'api',
    ]);

    expect(vol.existsSync('/project/my-api/src/routes.ts')).toBe(true);
  });

  it('respects --no-typescript flag', async () => {
    await initCommand.parseAsync([
      'node',
      'test',
      'my-app',
      '--no-typescript',
    ]);

    expect(vol.existsSync('/project/my-app/src/index.js')).toBe(true);
    expect(vol.existsSync('/project/my-app/tsconfig.json')).toBe(false);
  });

  it('shows dry run output without creating files', async () => {
    const consoleSpy = vi.spyOn(console, 'log');

    await initCommand.parseAsync([
      'node',
      'test',
      'my-app',
      '--dry-run',
    ]);

    expect(vol.existsSync('/project/my-app')).toBe(false);
    expect(consoleSpy).toHaveBeenCalledWith(
      expect.stringContaining('Dry run')
    );
  });
});
```

### Testing Interactive Prompts

```typescript
// tests/prompts/setup.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import prompts from 'prompts';
import { runInitPrompts } from '../../src/prompts/setup.js';

describe('runInitPrompts', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('returns user selections', async () => {
    // Inject test values
    prompts.inject(['my-project', 'api', true, 'pnpm', ['eslint'], true]);

    const result = await runInitPrompts();

    expect(result).toEqual({
      name: 'my-project',
      template: 'api',
      typescript: true,
      packageManager: 'pnpm',
      features: ['eslint'],
      git: true,
    });
  });

  it('uses defaults when provided', async () => {
    prompts.inject(['my-project', 'default', true, 'npm', [], true]);

    const result = await runInitPrompts({ typescript: true });

    expect(result.typescript).toBe(true);
  });

  it('throws CLIError when cancelled', async () => {
    // Simulate Ctrl+C
    prompts.inject([new Error('cancelled')]);

    await expect(runInitPrompts()).rejects.toThrow('Setup cancelled');
  });
});
```

### Testing Error Handling

```typescript
// tests/lib/errors.test.ts
import { describe, it, expect } from 'vitest';
import { CLIError, formatError } from '../../src/lib/errors.js';

describe('CLIError', () => {
  it('creates error with message and exit code', () => {
    const error = new CLIError('Test error', 2);

    expect(error.message).toBe('Test error');
    expect(error.exitCode).toBe(2);
    expect(error.name).toBe('CLIError');
  });

  it('creates validation error', () => {
    const error = CLIError.validation('name', 'string');

    expect(error.message).toContain('Invalid name');
    expect(error.exitCode).toBe(1);
  });

  it('creates file not found error', () => {
    const error = CLIError.fileNotFound('/path/to/file');

    expect(error.message).toContain('/path/to/file');
  });
});

describe('formatError', () => {
  it('formats CLIError with details', () => {
    const error = new CLIError('Main error', 1, 'Additional details');
    const formatted = formatError(error);

    expect(formatted).toContain('Main error');
    expect(formatted).toContain('Additional details');
  });

  it('formats generic Error', () => {
    const error = new Error('Generic error');
    const formatted = formatError(error);

    expect(formatted).toContain('Generic error');
  });

  it('formats non-Error values', () => {
    const formatted = formatError('string error');

    expect(formatted).toContain('string error');
  });
});
```

### Integration Tests

```typescript
// tests/integration/cli.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { execSync } from 'node:child_process';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

describe('CLI integration', () => {
  let testDir: string;
  const cliPath = join(__dirname, '../../dist/index.js');

  beforeAll(() => {
    testDir = mkdtempSync(join(tmpdir(), 'cli-test-'));
  });

  afterAll(() => {
    rmSync(testDir, { recursive: true, force: true });
  });

  const runCLI = (args: string): string => {
    return execSync(`node ${cliPath} ${args}`, {
      cwd: testDir,
      encoding: 'utf-8',
    });
  };

  it('shows help with --help', () => {
    const output = runCLI('--help');

    expect(output).toContain('Usage:');
    expect(output).toContain('Commands:');
  });

  it('shows version with --version', () => {
    const output = runCLI('--version');

    expect(output).toMatch(/\d+\.\d+\.\d+/);
  });

  it('creates project with init command', () => {
    const output = runCLI('init test-project --template default --no-git');

    expect(output).toContain('created successfully');
  });

  it('exits with error for unknown command', () => {
    expect(() => runCLI('unknown-command')).toThrow();
  });
});
```

## 9. Publishing to npm

### Prepare for Publishing

```typescript
// scripts/prepublish.ts
import { execSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';

// Ensure clean build
execSync('npm run build', { stdio: 'inherit' });

// Run tests
execSync('npm test', { stdio: 'inherit' });

// Verify package.json
const pkg = JSON.parse(readFileSync('package.json', 'utf-8'));

const required = ['name', 'version', 'description', 'bin', 'files'];
for (const field of required) {
  if (!pkg[field]) {
    console.error(`Missing required field: ${field}`);
    process.exit(1);
  }
}

console.log('Ready to publish!');
```

### package.json Publishing Configuration

```json
{
  "name": "@scope/my-cli",
  "version": "1.0.0",
  "description": "A production CLI tool",
  "keywords": ["cli", "tool", "automation"],
  "author": "Your Name <email@example.com>",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/username/my-cli.git"
  },
  "bugs": {
    "url": "https://github.com/username/my-cli/issues"
  },
  "homepage": "https://github.com/username/my-cli#readme",
  "type": "module",
  "bin": {
    "my-cli": "./dist/index.js"
  },
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    }
  },
  "files": [
    "dist",
    "templates"
  ],
  "scripts": {
    "prepublishOnly": "npm run build && npm test"
  },
  "publishConfig": {
    "access": "public"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

### Release Script

```typescript
// scripts/release.ts
import { execSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';
import prompts from 'prompts';
import chalk from 'chalk';

async function release() {
  const pkg = JSON.parse(readFileSync('package.json', 'utf-8'));
  const currentVersion = pkg.version;

  console.log(chalk.blue(`Current version: ${currentVersion}`));

  const { releaseType } = await prompts({
    type: 'select',
    name: 'releaseType',
    message: 'Select release type:',
    choices: [
      { title: 'Patch', value: 'patch' },
      { title: 'Minor', value: 'minor' },
      { title: 'Major', value: 'major' },
    ],
  });

  if (!releaseType) {
    console.log(chalk.yellow('Release cancelled'));
    return;
  }

  // Run tests first
  console.log(chalk.blue('Running tests...'));
  execSync('npm test', { stdio: 'inherit' });

  // Build
  console.log(chalk.blue('Building...'));
  execSync('npm run build', { stdio: 'inherit' });

  // Bump version
  console.log(chalk.blue(`Bumping ${releaseType} version...`));
  execSync(`npm version ${releaseType} --no-git-tag-version`, {
    stdio: 'inherit',
  });

  const newPkg = JSON.parse(readFileSync('package.json', 'utf-8'));
  const newVersion = newPkg.version;

  // Git commit and tag
  execSync('git add package.json package-lock.json', { stdio: 'inherit' });
  execSync(`git commit -m "chore: release v${newVersion}"`, {
    stdio: 'inherit',
  });
  execSync(`git tag v${newVersion}`, { stdio: 'inherit' });

  // Confirm publish
  const { confirmPublish } = await prompts({
    type: 'confirm',
    name: 'confirmPublish',
    message: `Publish v${newVersion} to npm?`,
    initial: true,
  });

  if (confirmPublish) {
    execSync('npm publish', { stdio: 'inherit' });
    execSync('git push && git push --tags', { stdio: 'inherit' });
    console.log(chalk.green(`Published v${newVersion}!`));
  } else {
    console.log(chalk.yellow('Publish cancelled. Git changes preserved.'));
  }
}

release().catch(console.error);
```

### GitHub Actions for Publishing

```yaml
# .github/workflows/publish.yml
name: Publish to npm

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build

      - name: Publish
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Post-Install Script

```typescript
// scripts/postinstall.ts
import chalk from 'chalk';

const message = `
${chalk.green('Thank you for installing my-cli!')}

Get started:
  ${chalk.cyan('my-cli init my-project')}    Create a new project
  ${chalk.cyan('my-cli --help')}             Show all commands

Documentation: https://github.com/username/my-cli
`;

console.log(message);
```

### Executable Verification

```bash
# In package.json scripts
"postbuild": "chmod +x dist/index.js"
```

After building, verify the CLI works:

```bash
# Link locally for testing
npm link

# Test the CLI
my-cli --version
my-cli --help
my-cli init test-project

# Unlink when done
npm unlink -g my-cli
```
