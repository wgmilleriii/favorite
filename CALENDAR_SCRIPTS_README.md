# Calendar Script Documentation

## Overview

These scripts allow you to easily check your Gazelle piano tuning calendar for upcoming appointments. The system consists of two files:

1. `view_calendar.py` - Python script that downloads and parses the ICS calendar file
2. `check_calendar.sh` - Bash script wrapper for easy execution

## Prerequisites

- Python 3.x
- The following Python packages (automatically installed by the script):
  - requests
  - icalendar
  - pytz

## Usage

### Quick Check

Run the bash script from your terminal:

```bash
./check_calendar.sh
```

This will:
- Install required Python dependencies if needed
- Download your calendar from the Gazelle ICS URL
- Show tomorrow's appointments in a formatted display

### Direct Python Usage

You can also run the Python script directly:

```bash
python3 view_calendar.py
```

## Calendar Data Source

The script is configured to use your Gazelle piano tuning calendar:
```
https://gazelleapp.io/calendars/cal_BM7FwKln8bo6rZpqgShFT7CD0pPchDfS3mZ25UvCDxcx.ics
```

## Features

- Displays appointments for tomorrow only
- Shows appointment time, title, location and partial description
- Color-coded output in the shell script for better readability
- Handles all-day events appropriately
- Sorts events chronologically

## Customization

To modify the script to show a different date range or calendar:

1. Edit `view_calendar.py`
2. Change the `ics_url` variable to point to a different calendar
3. Modify the `get_tomorrow_events()` function to display different dates

## Troubleshooting

If you encounter issues:

1. Ensure you have Python 3 installed
2. Check your internet connection (required to download the calendar)
3. Verify the ICS URL is still valid

---

*Note: This script only displays calendar information and does not modify your calendar in any way.* 