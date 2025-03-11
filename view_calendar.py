#!/usr/bin/env python3
"""
Calendar ICS Parser - Shows events for tomorrow from an ICS file
"""
import sys
import requests
from datetime import datetime, timedelta
from icalendar import Calendar
import pytz

def download_ics(url):
    """Download ICS file from URL"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error downloading calendar: {e}")
        sys.exit(1)

def parse_calendar(ics_data):
    """Parse ICS data into Calendar object"""
    try:
        return Calendar.from_ical(ics_data)
    except Exception as e:
        print(f"Error parsing calendar data: {e}")
        sys.exit(1)

def get_tomorrow_events(calendar):
    """Extract tomorrow's events from calendar"""
    # Calculate tomorrow's date
    tomorrow = datetime.now().date() + timedelta(days=1)
    tomorrow_start = datetime.combine(tomorrow, datetime.min.time()).replace(tzinfo=pytz.UTC)
    tomorrow_end = datetime.combine(tomorrow, datetime.max.time()).replace(tzinfo=pytz.UTC)
    
    events = []
    
    for component in calendar.walk():
        if component.name == "VEVENT":
            # Get event start time
            start = component.get('dtstart').dt
            
            # Handle all-day events (date objects)
            if isinstance(start, datetime):
                event_date = start.date()
            else:
                event_date = start
                
            # Check if event is tomorrow
            if event_date == tomorrow.date():
                # Extract event details
                summary = str(component.get('summary', 'No Title'))
                
                # Format time for display
                if isinstance(start, datetime):
                    start_time = start.strftime('%I:%M %p')
                else:
                    start_time = "All day"
                
                # Add location if available
                location = component.get('location', '')
                if location:
                    location = f" at {location}"
                    
                # Add description if available
                description = component.get('description', '')
                if description:
                    # Truncate description if too long
                    if len(description) > 100:
                        description = description[:97] + "..."
                
                events.append({
                    'start_time': start_time,
                    'summary': summary,
                    'location': location,
                    'description': description
                })
    
    # Sort events by start time
    events.sort(key=lambda x: x['start_time'])
    
    return events

def display_events(events, date):
    """Display events in a formatted way"""
    print(f"\n📅 SCHEDULE FOR {date.strftime('%A, %B %d, %Y').upper()}")
    print("=" * 60)
    
    if not events:
        print("No events scheduled for tomorrow.")
    else:
        for i, event in enumerate(events, 1):
            print(f"{i}. {event['start_time']} - {event['summary']}{event['location']}")
            if event['description']:
                print(f"   Details: {event['description']}")
            print()
    
    print("=" * 60)

def main():
    # Calendar URL
    ics_url = "https://gazelleapp.io/calendars/cal_BM7FwKln8bo6rZpqgShFT7CD0pPchDfS3mZ25UvCDxcx.ics"
    
    print("Downloading calendar data...")
    ics_data = download_ics(ics_url)
    
    print("Parsing calendar...")
    calendar = parse_calendar(ics_data)
    
    print("Finding tomorrow's events...")
    tomorrow = datetime.now().date() + timedelta(days=1)
    events = get_tomorrow_events(calendar)
    
    display_events(events, tomorrow)
    
if __name__ == "__main__":
    main() 