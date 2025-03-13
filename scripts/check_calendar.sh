#!/bin/bash
# Simple script to check tomorrow's calendar events

# Define colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== PIANO SCHEDULE CHECKER ===${NC}"
echo -e "${BLUE}Checking for tomorrow's appointments...${NC}"

# Install required Python packages if not already installed
echo "Checking for required Python packages..."
pip install -q requests icalendar pytz

# Run the Python script
python3 view_calendar.py

echo -e "\n${GREEN}You can use this script at any time to check your calendar.${NC}"
echo -e "${BLUE}Usage: ./check_calendar.sh${NC}" 