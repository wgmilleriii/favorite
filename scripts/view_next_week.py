#!/usr/bin/env python3
"""
Calendar ICS Parser - Shows events for next week from an ICS file
"""
import sys
import json
import os
import requests
from datetime import datetime, timedelta
from icalendar import Calendar
import pytz

CACHE_FILE = "calendar_cache.json"
CACHE_EXPIRY_HOURS = 1  # Cache expires after 1 hour

def load_cache():
    """Load cached calendar data if available and not expired"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                cache = json.load(f)
                last_updated = datetime.fromisoformat(cache['last_updated'])
                if datetime.now() - last_updated < timedelta(hours=CACHE_EXPIRY_HOURS):
                    print(f"Using cached data (last updated: {last_updated.strftime('%I:%M %p')})")
                    return cache['data']
        except Exception as e:
            print(f"Cache read error: {e}")
    return None

def save_cache(data):
    """Save calendar data to cache file"""
    try:
        cache = {
            'last_updated': datetime.now().isoformat(),
            'data': data
        }
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f)
    except Exception as e:
        print(f"Cache write error: {e}")

def download_ics(url):
    """Download ICS file from URL or use cache"""
    cached_data = load_cache()
    if cached_data:
        return cached_data
        
    try:
        print("Downloading fresh calendar data...")
        response = requests.get(url)
        response.raise_for_status()
        data = response.text
        save_cache(data)
        return data
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

def get_next_week_events(calendar):
    """Extract next week's events from calendar"""
    # Calculate date range for next week
    today = datetime.now().date()
    next_week_start = today + timedelta(days=(7 - today.weekday()))
    next_week_end = next_week_start + timedelta(days=6)
    
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
                
            # Check if event is in next week
            if next_week_start <= event_date <= next_week_end:
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
                    'date': event_date,
                    'start_time': start_time,
                    'summary': summary,
                    'location': location,
                    'description': description
                })
    
    # Sort events by date and time
    events.sort(key=lambda x: (x['date'], x['start_time']))
    
    return events

def display_events(events, start_date, end_date):
    """Display events in a formatted way"""
    print(f"\n📅 SCHEDULE FOR WEEK OF {start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}")
    print("=" * 80)
    
    if not events:
        print("No events scheduled for next week.")
    else:
        current_date = None
        for event in events:
            # Print date header when date changes
            if current_date != event['date']:
                current_date = event['date']
                print(f"\n{current_date.strftime('%A, %B %d')}:")
                print("-" * 40)
            
            print(f"  • {event['start_time']} - {event['summary']}{event['location']}")
            if event['description']:
                print(f"    Details: {event['description']}")
    
    print("\n" + "=" * 80)

def main():
    # Calendar URL
    ics_url = "https://gazelleapp.io/calendars/cal_BM7FwKln8bo6rZpqgShFT7CD0pPchDfS3mZ25UvCDxcx.ics"
    
    ics_data = download_ics(ics_url)
    
    print("Parsing calendar...")
    calendar = parse_calendar(ics_data)
    
    print("Finding next week's events...")
    today = datetime.now().date()
    next_week_start = today + timedelta(days=(7 - today.weekday()))
    next_week_end = next_week_start + timedelta(days=6)
    events = get_next_week_events(calendar)
    
    display_events(events, next_week_start, next_week_end)

if __name__ == "__main__":
    main() 