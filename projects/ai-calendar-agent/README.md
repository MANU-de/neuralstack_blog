# AI Calendar Agent (Pure Python)

This simple CLI agent lets you add, list, and delete calendar events using natural-language prompts. Everything lives in a single Python file that depends only on the standard library, so you can drop it into any workflow or extend it as needed.

## Features

- `add meeting with Sara tomorrow at 10:30`
- `view events on 2025-01-15`
- `show upcoming events`
- `delete event 3`
- Helpful `help` command that documents capabilities

## Project Layout

```
ai-calendar-agent/
├── calendar_agent.py  # Agent logic + command loop
└── README.md          # This file
```

## Quick Start

```bash
cd neuralstack_blog/projects/ai-calendar-agent
python calendar_agent.py
```

When prompted, type commands like the ones above. Use `exit` to quit.

## Extending

- Replace the in-memory list with a database or API for persistence.
- Add more regex patterns in `process_command` for richer interactions.
- Import the helper functions from other agents or automation workflows.

Enjoy hacking on it! 🎉

