---
name: custom-agents:work
description: Execute tasks from an epic with re-anchoring and optional review
argument-hint: "<epic-id or task-id> [--yolo]"
---

# IMPORTANT: This command MUST invoke the skill `custom-agents-work`

The ONLY purpose of this command is to call the `custom-agents-work` skill. You MUST use that skill now.

**User input:** $ARGUMENTS

Pass the user input to the skill. The skill handles all execution logic including worker spawning.

**CRITICAL RULES:**
1. Do NOT read files directly - the skill spawns workers for that
2. Do NOT edit files directly - workers handle implementation
3. Do NOT use TodoWrite - use taskctl via the skill
4. You MUST spawn worker subagents for each task - never implement directly
