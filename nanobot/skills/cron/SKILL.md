---
name: cron
description: Schedule reminders and recurring tasks with two delivery modes.
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
cron(action="add", message="Check HKUDS/nanobot GitHub stars and report the count", every_seconds=3600, deliver=False)

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
| "every 20 minutes" | `every_seconds: 1200` |
| "every hour" | `every_seconds: 3600` |
| "every 2 hours" | `every_seconds: 7200` |
| "every day at 8am" | `cron_expr: "0 8 * * *"` |
| "weekdays at 5pm" | `cron_expr: "0 17 * * 1-5"` |
| "every Monday at 9am" | `cron_expr: "0 9 * * 1"` |
| "9am Vancouver time daily" | `cron_expr: "0 9 * * *", tz: "America/Vancouver"` |
| "at 3pm today" | `at: <compute with date command>` |
| "tomorrow at 10am" | `at: <compute with date command>` |

---

## Decision Guide

**Ask yourself:**

1. **Does this need action/processing?**
   - No → `deliver=True` (simple reminder)
   - Yes → `deliver=False` (agent task)

2. **Is the message itself the complete notification?**
   - Yes → `deliver=True`
   - No, agent needs to do something → `deliver=False`

3. **Should I save tokens?**
   - Yes → `deliver=True` (skips agent)
   - No, need processing → `deliver=False`

---

## Common Patterns

### ✅ Good for `deliver=True` (Direct)
```
- "Take your medicine"
- "Stretch break"
- "Lunch time"
- "Submit timesheet"
- "Call mom"
```

### ✅ Good for `deliver=False` (Agent)
```
- "Fetch latest stock prices for AAPL, GOOGL, TSLA"
- "Check if there are new issues in HKUDS/nanobot repo"
- "Run health check on all services and log results"
- "Summarize top 3 news headlines"
- "Backup database and verify integrity"
```

---

## Timezone Reference

Common IANA timezones:
- `America/New_York` - Eastern Time
- `America/Chicago` - Central Time
- `America/Denver` - Mountain Time
- `America/Los_Angeles` - Pacific Time
- `America/Vancouver` - Pacific Time (Canada)
- `Europe/London` - GMT/BST
- `Europe/Paris` - Central European Time
- `Asia/Tokyo` - Japan Standard Time
- `Asia/Shanghai` - China Standard Time
- `Asia/Kolkata` - India Standard Time
- `Australia/Sydney` - Australian Eastern Time

---

## Important Notes

1. **Prevents infinite loops**: Cron jobs cannot schedule other cron jobs
2. **One-time jobs**: Auto-disable after running (use `every_seconds` or `cron_expr` for recurring)
3. **Timezone**: Only applies to `cron_expr`, not to `every_seconds` or `at`
4. **Message length**: Keep messages concise (truncated to 30 chars for job name)
