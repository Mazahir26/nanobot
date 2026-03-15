---
name: cron
description: Schedule reminders and recurring tasks with two delivery modes. Use this skill whenever the user asks to set a reminder, schedule a task, create a recurring notification, or mentions anything about timing like "remind me", "every day", "schedule", "at 5pm", "in 2 hours", "daily", "weekly", "cron", "timer", or "alarm". Also use when user wants automated periodic checks or recurring agent tasks.
metadata: {"nanobot":{"emoji":"⏰","always":false}}
---

# Cron - Scheduled Tasks & Reminders

Use the `cron` tool to schedule reminders or recurring tasks. 

## Two Delivery Modes

### Mode 1: `deliver=true` (SIMPLE REMINDER) - DEFAULT
**Use for:** Basic notifications that don't need processing.

- Message is sent **directly to user** at trigger time
- **No agent processing** (saves tokens, instant delivery)
- The exact message is delivered as-is

**Examples:**
- "Drink water"
- "Take a break"
- "Meeting in 5 minutes"
- "Time for your daily walk"

### Mode 2: `deliver=false` (COMPLEX TASK)
**Use for:** Tasks requiring agent action/processing.

- **Agent processes** the task at trigger time
- Agent executes instructions (fetch data, run commands, update files)
- Agent's response is delivered to user

**Examples:**
- "Check GitHub stars and report"
- "Fetch weather forecast"
- "Run backup script and log results"
- "Summarize today's news"

---

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | string | `"add"`, `"list"`, or `"remove"` |
| `message` | string | The reminder/task instruction |
| `deliver` | boolean | **TRUE** (default): Direct delivery. **FALSE**: Agent processes |
| `every_seconds` | integer | Interval in seconds (recurring) |
| `cron_expr` | string | Cron expression like `"0 9 * * *"` |
| `tz` | string | IANA timezone (e.g., `"America/Vancouver"`) - only with `cron_expr` |
| `at` | string | ISO datetime for one-time execution |
| `job_id` | string | Job ID for removal |

---

## Computing Time - Use `date` Command

**Before scheduling, compute the current time or target datetime:**

```bash
# Get current date/time
date
# Output: Wed Mar 4 10:30 AM UTC 2026

# Get current ISO format
date -Iseconds
# Output: 2026-03-04T10:30:00+00:00

# Calculate "2 hours from now" in ISO format
date -d "+2 hours" -Iseconds
# Output: 2026-03-04T12:30:00+00:00

# Calculate "today at 5pm" in ISO format
date -d "today 17:00" -Iseconds
# Output: 2026-03-04T17:00:00+00:00

# Calculate "tomorrow at 9am" in ISO format
date -d "tomorrow 09:00" -Iseconds
# Output: 2026-03-05T09:00:00+00:00
```

**For one-time reminders:**
1. Run `date -d "<target time>" -Iseconds` to get ISO datetime
2. Use the output in the `at` parameter

---

## Examples

### Simple Reminder (Direct Delivery)
```python
# Drink water reminder every 2 hours
cron(action="add", message="💧 Time to drink water!", every_seconds=7200, deliver=True)

# Daily standup reminder at 9am (simple notification)
cron(action="add", message="📅 Daily standup meeting!", cron_expr="0 9 * * *", deliver=True)

# One-time reminder at specific time
cron(action="add", message="📞 Call John!", at="2026-03-04T17:00:00+00:00", deliver=True)
```

### Complex Task (Agent Processing)
```python
# Check GitHub stars every hour (agent fetches and reports)
cron(action="add", message="Check GitHub stars for HKUDS/nanobot and report the count", every_seconds=3600, deliver=False)

# Fetch weather forecast every morning
cron(action="add", message="Get weather forecast for today and summarize", cron_expr="0 8 * * *", deliver=False)

# Run backup and log results
cron(action="add", message="Run backup script and save results to backup.log", cron_expr="0 2 * * *", deliver=False)
```

### List and Remove Jobs
```python
# List all scheduled jobs
cron(action="list")

# Remove a specific job
cron(action="remove", job_id="abc123")
```

---

## Time Expressions Reference

| User Request | Parameters |
|--------------|------------|
| "Remind me in 30 minutes" | `at="2026-03-04T11:00:00"` (compute from current time) |
| "Every hour" | `every_seconds=3600` |
| "Every day at 9am" | `cron_expr="0 9 * * *"` |
| "Every Monday at 10am" | `cron_expr="0 10 * * 1"` |
| "Every weekday at 9am" | `cron_expr="0 9 * * 1-5"` |
| "First day of month" | `cron_expr="0 9 1 * *"` |

---

## Common Patterns

### Daily Health Reminders
```python
cron(action="add", message="💧 Drink water!", every_seconds=7200)  # Every 2 hours
cron(action="add", message="🧘 Take a stretch break!", every_seconds=5400)  # Every 90 min
cron(action="add", message="💧 Time to hydrate!", cron_expr="0 10,14,18 * * *")  # 10am, 2pm, 6pm
```

### Work Reminders
```python
cron(action="add", message="📅 Standup meeting!", cron_expr="0 9 * * 1-5")  # Weekdays 9am
cron(action="add", message="📋 Review today's tasks", cron_expr="0 9 * * *")  # Daily 9am
cron(action="add", message="📝 End of day summary", cron_expr="0 17 * * 1-5")  # Weekdays 5pm
```

### Recurring Tasks
```python
cron(action="add", message="Check GitHub issues and prioritize", cron_expr="0 10 * * 1", deliver=False)  # Monday 10am
cron(action="add", message="Summarize this week's progress", cron_expr="0 16 * * 5", deliver=False)  # Friday 4pm
```

---

## Notes

- **Always compute time** using `date` command before scheduling one-time reminders
- **Timezone:** Use `tz` parameter with cron expressions for timezone-aware scheduling
- **One-time jobs** automatically delete after execution
- **Infinite loop prevention:** The agent cannot schedule new cron jobs while executing a cron task