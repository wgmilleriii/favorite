# 🚀 Quick Command Reference
*A guide to all shortcut commands in the system*

## Daily Workflow Commands

### 🌅 Start of Day
```bash
GOODMORNING
```
- Triggers SNOOP process
- Checks for updates
- Reviews TODO files

### 👀 SNOOP Commands
```bash
SNOOP                 # Check NEIGHBOR's progress
SHARESNOOP           # Share SNOOP executable
DUMPTONEIGHBOR       # Copy .cursorrules to NEIGHBOR
```
**SNOOP Process:**
1. Goes up one directory level
2. Locates neighbor's git repo
3. Updates NEIGHBOR_TODO.md
4. Compares .cursorrules

### 🔍 Check Commands
```bash
CHECKIN              # Show 15-min goals & open docs
CURL [url]           # Fetch and display website content
```

### ❓ Question Commands
```bash
command?             # Get clarification
command??            # Get detailed clarification
command!             # Simplify and explain issues
```

### 🌙 End of Day
```bash
BYEBYE               # Prepare for shutdown
```
- Updates git
- Documents next steps
- Logs productivity

## Timer Commands
```bash
TIMER 20             # Set 20-minute timer
TIMER 60             # Set 1-hour timer
```
*Note: Only Katie can set timers*

## File Management
```bash
TODO_MAC            # MAC-specific tasks
TODO_PC             # PC-specific tasks
```

## Logging Format
All commands are logged in `instructions.txt` with:
```
[TIMESTAMP] [PC/MAC]
Command: <original command>
Interpretation: <what it means>
Changes: <what happened>
```

## Examples

### Good Usage:
```bash
GOODMORNING
> Checking NEIGHBOR's progress...
> Updated NEIGHBOR_TODO.md
> Found 3 new updates

SNOOP
> Inspecting neighbor's repo...
> Differences found in .cursorrules
> Generated comparison report

BYEBYE
> Committing changes...
> Documented next steps
> Ready for shutdown
```

### Common Patterns:
1. Start day: `GOODMORNING`
2. Check progress: `SNOOP`
3. Regular check-ins: `CHECKIN`
4. End day: `BYEBYE`

## Tips
- Use `CHECKIN` every 15 minutes to stay focused
- `SNOOP` before making major changes
- End questions with `?` or `??` for different detail levels
- Use `!` when something goes wrong

## Neighbor Integration
- Neighbor's repo is one level up
- Similar .cursorrules expected
- Use `DUMPTONEIGHBOR` carefully

*Last Updated: March 13, 2024* 