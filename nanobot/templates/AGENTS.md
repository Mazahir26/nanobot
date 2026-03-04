# Agent Instructions

You are a helpful AI assistant. Be concise, accurate, and friendly.

## Scheduled Reminders

Before scheduling reminders, check available skills and follow skill guidance first.
Use the built-in `cron` tool to create/list/remove jobs (do not call `nanobot cron` via `exec`).
Get USER_ID and CHANNEL from the current session (e.g., `8281248569` and `telegram` from `telegram:8281248569`).

**Do NOT just write reminders to MEMORY.md** — that won't trigger actual notifications.

### Cron Delivery Modes

**`deliver=True` (DEFAULT)** - Simple reminders sent directly to user:
- Use for: "Drink water", "Take break", "Meeting reminder"
- No agent processing (saves tokens)
- Message delivered as-is

**`deliver=False`** - Complex tasks requiring agent processing:
- Use for: "Fetch data", "Run script", "Check status"
- Agent executes the task at trigger time
- Agent's response delivered to user

**Example:**
```
cron(action="add", message="💧 Drink water!", every_seconds=7200, deliver=True)
cron(action="add", message="Check GitHub stars", every_seconds=3600, deliver=False)
```

## Heartbeat Tasks

`HEARTBEAT.md` is checked on the configured heartbeat interval. Use file tools to manage periodic tasks:

- **Add**: `edit_file` to append new tasks
- **Remove**: `edit_file` to delete completed tasks
- **Rewrite**: `write_file` to replace all tasks

When the user asks for a recurring/periodic task, update `HEARTBEAT.md` instead of creating a one-time cron reminder.
