#!/usr/bin/env python3
"""
Calendar ICS Parser - Shows events for the next month from an ICS file
"""
import sys
import requests
from datetime import datetime, timedelta
from icalendar import Calendar
import pytz
from collections import defaultdict

def download_ics(url):
    """Download ICS file from URL"""
    try:
        response = requests.get(url)
        response.raise_for_status()
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

def get_month_events(calendar):
    """Extract next month's events from calendar"""
    # Calculate date range for next month
    today = datetime.now().date()
    end_date = today + timedelta(days=31)
    
    events_by_date = defaultdict(list)
    
    for component in calendar.walk():
        if component.name == "VEVENT":
            try:
                # Get event start time
                start = component.get('dtstart').dt
                
                # Handle all-day events (date objects)
                if isinstance(start, datetime):
                    event_date = start.date()
                    start_time = start.strftime('%I:%M %p')
                else:
                    event_date = start
                    start_time = "All day"
                
                # Only process events within our date range
                if today <= event_date <= end_date:
                    # Extract event details
                    summary = str(component.get('summary', 'No Title'))
                    location = str(component.get('location', ''))
                    description = str(component.get('description', ''))
                    
                    # Get end time if available
                    end = component.get('dtend')
                    if end:
                        end = end.dt
                        if isinstance(end, datetime):
                            end_time = end.strftime('%I:%M %p')
                        else:
                            end_time = "All day"
                    else:
                        end_time = None
                    
                    # Format duration if available
                    duration = None
                    if isinstance(start, datetime) and isinstance(end, datetime):
                        duration = end - start
                        
                    event = {
                        'start_time': start_time,
                        'end_time': end_time,
                        'summary': summary,
                        'location': location,
                        'description': description,
                        'duration': duration,
                        'date': event_date
                    }
                    
                    events_by_date[event_date].append(event)
            except Exception as e:
                print(f"Error processing event: {e}")
                continue
    
    return events_by_date

def display_events(events_by_date):
    """Display events in a formatted way"""
    print(f"\n📅 CALENDAR EVENTS FOR THE NEXT MONTH")
    print("=" * 80)
    
    if not events_by_date:
        print("No events scheduled for the next month.")
        return
    
    # Sort dates
    sorted_dates = sorted(events_by_date.keys())
    
    for date in sorted_dates:
        print(f"\n{date.strftime('%A, %B %d, %Y')}:")
        print("-" * 40)
        
        # Sort events by start time
        events = sorted(events_by_date[date], key=lambda x: x['start_time'])
        
        for i, event in enumerate(events, 1):
            print(f"{i}. {event['start_time']} - {event['summary']}")
            
            if event['location']:
                print(f"   Location: {event['location']}")
            
            if event['end_time']:
                print(f"   End time: {event['end_time']}")
            
            if event['duration']:
                hours = event['duration'].total_seconds() / 3600
                print(f"   Duration: {hours:.1f} hours")
            
            if event['description']:
                print(f"   Details: {event['description']}")
            
            print()  # Empty line between events
    
    print("=" * 80)
    print(f"Calendar data retrieved at: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}")

def main():
    # Calendar URL
    ics_url = "https://gazelleapp.io/calendars/cal_BM7FwKln8bo6rZpqgShFT7CD0pPchDfS3mZ25UvCDxcx.ics"
    
    print("Downloading calendar data...")
    try:
        ics_data = download_ics(ics_url)
    except Exception as e:
        print(f"Failed to download calendar: {e}")
        sys.exit(1)
    
    print("Parsing calendar...")
    try:
        calendar = parse_calendar(ics_data)
    except Exception as e:
        print(f"Failed to parse calendar: {e}")
        sys.exit(1)
    
    print("Finding events for the next month...")
    try:
        events = get_month_events(calendar)
        display_events(events)
    except Exception as e:
        print(f"Error displaying events: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 