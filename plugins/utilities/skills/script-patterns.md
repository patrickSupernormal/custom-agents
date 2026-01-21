---
skill: script-patterns
version: "1.0.0"
description: "Common scripting patterns and templates for automation and utility tasks"
used-by: ["@script-writer", "@automation-engineer", "@devops-specialist", "@general-dev"]
---

# Script Patterns Skill

## Overview
Reusable patterns for common scripting tasks across shell, Node.js, and Python environments.

## Shell Script Templates

### Basic Script Structure
```bash
#!/bin/bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG_FILE="${SCRIPT_DIR}/script.log"

# Logging
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"; }
error() { log "ERROR: $*" >&2; exit 1; }

# Argument parsing
usage() {
    cat <<EOF
Usage: $(basename "$0") [options] <argument>
Options:
    -h, --help      Show this help
    -v, --verbose   Verbose output
    -d, --dry-run   Show what would be done
EOF
}

VERBOSE=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help) usage; exit 0 ;;
        -v|--verbose) VERBOSE=true; shift ;;
        -d|--dry-run) DRY_RUN=true; shift ;;
        *) break ;;
    esac
done

# Main logic
main() {
    log "Starting script..."
    # Your code here
    log "Complete."
}

main "$@"
```

### File Processing Pattern
```bash
#!/bin/bash
set -euo pipefail

process_file() {
    local file="$1"
    # Process logic here
    echo "Processing: $file"
}

# Find and process files
find "${1:-.}" -type f -name "*.txt" | while read -r file; do
    process_file "$file"
done
```

### Cleanup Trap Pattern
```bash
#!/bin/bash
TEMP_DIR=""

cleanup() {
    [[ -n "$TEMP_DIR" && -d "$TEMP_DIR" ]] && rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

TEMP_DIR=$(mktemp -d)
# Use $TEMP_DIR safely - it will be cleaned up on exit
```

## Node.js Script Templates

### CLI Tool Pattern
```typescript
#!/usr/bin/env npx ts-node
import { parseArgs } from 'node:util';
import { readFileSync, writeFileSync } from 'node:fs';

interface Options {
  input: string;
  output: string;
  verbose: boolean;
}

const { values } = parseArgs({
  options: {
    input: { type: 'string', short: 'i' },
    output: { type: 'string', short: 'o' },
    verbose: { type: 'boolean', short: 'v', default: false },
  },
});

const options = values as unknown as Options;

async function main() {
  if (!options.input) {
    console.error('Usage: script.ts -i <input> -o <output>');
    process.exit(1);
  }

  const data = readFileSync(options.input, 'utf-8');
  // Process data
  const result = transform(data);

  if (options.output) {
    writeFileSync(options.output, result);
  } else {
    console.log(result);
  }
}

function transform(data: string): string {
  // Transform logic
  return data.toUpperCase();
}

main().catch(console.error);
```

### Batch Processing Pattern
```typescript
import pLimit from 'p-limit';

const limit = pLimit(5); // Max 5 concurrent

async function processBatch<T, R>(
  items: T[],
  processor: (item: T) => Promise<R>,
  concurrency = 5
): Promise<R[]> {
  const limiter = pLimit(concurrency);
  return Promise.all(
    items.map(item => limiter(() => processor(item)))
  );
}

// Usage
const results = await processBatch(
  urls,
  async (url) => fetch(url).then(r => r.json()),
  10
);
```

### File Watcher Pattern
```typescript
import { watch } from 'chokidar';

const watcher = watch('src/**/*.ts', {
  ignored: /node_modules/,
  persistent: true,
});

watcher
  .on('add', path => console.log(`Added: ${path}`))
  .on('change', path => console.log(`Changed: ${path}`))
  .on('unlink', path => console.log(`Removed: ${path}`));

// Graceful shutdown
process.on('SIGINT', () => {
  watcher.close();
  process.exit(0);
});
```

## Python Script Templates

### CLI with Click Pattern
```python
#!/usr/bin/env python3
import click
from pathlib import Path

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('-o', '--output', type=click.Path(), help='Output file')
@click.option('-v', '--verbose', is_flag=True, help='Verbose output')
def main(input_path: str, output: str, verbose: bool):
    """Process INPUT_PATH and optionally write to output."""
    data = Path(input_path).read_text()
    result = process(data)

    if output:
        Path(output).write_text(result)
        if verbose:
            click.echo(f'Written to {output}')
    else:
        click.echo(result)

def process(data: str) -> str:
    return data.upper()

if __name__ == '__main__':
    main()
```

## Decision Criteria

### Language Selection
| Use Case | Recommended |
|----------|-------------|
| File operations, git, system | Bash |
| JSON/API processing | Node.js |
| Data transformation | Python |
| Cross-platform CLI | Node.js + pkg |
| Quick one-liners | Bash |
| Complex async workflows | Node.js |

### Pattern Selection
| Need | Pattern |
|------|---------|
| Concurrent processing | Batch with p-limit |
| File watching | Chokidar watcher |
| Cleanup required | Trap pattern |
| User interaction | CLI with parseArgs/Click |
| Error handling | try/catch with logging |

## Common Pitfalls to Avoid

1. **Missing error handling** - Always use `set -e` in bash, try/catch in JS
2. **No cleanup on failure** - Use trap patterns for temp files
3. **Hardcoded paths** - Use `__dirname` or `$SCRIPT_DIR`
4. **Ignoring exit codes** - Check `$?` or use `-e` flag
5. **Unbounded concurrency** - Always limit parallel operations
6. **No logging** - Include timestamps and log levels
7. **Missing shebang** - Always include `#!/bin/bash` or `#!/usr/bin/env`

## Testing Scripts

### Bash Testing Pattern
```bash
# test_script.sh
#!/bin/bash
set -e

test_basic_functionality() {
    result=$(./script.sh --input test.txt)
    [[ "$result" == "expected" ]] || { echo "FAIL: basic"; exit 1; }
    echo "PASS: basic"
}

test_error_handling() {
    if ./script.sh --invalid 2>/dev/null; then
        echo "FAIL: should error on invalid input"
        exit 1
    fi
    echo "PASS: error handling"
}

test_basic_functionality
test_error_handling
echo "All tests passed!"
```

## Output Conventions

Scripts should output in consistent formats:
```bash
# For human consumption
echo "Processing 10 files..."
echo "  - file1.txt: OK"
echo "  - file2.txt: ERROR (reason)"
echo "Complete: 9 succeeded, 1 failed"

# For machine consumption (use --json flag)
echo '{"processed": 10, "success": 9, "failed": 1}'
```
