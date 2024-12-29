import csv
import os
from datetime import datetime, timedelta
from ics import Calendar, Event
import json
import pytz

def load_shifts(shift_file):
    """Load shifts from a JSON file."""
    with open(shift_file, 'r') as file:
        return json.load(file)

def create_ics_from_csv(csv_file, shift_file, output_file):
    """Generate an ICS file from a CSV file and a shift JSON file."""
    # Load shifts data
    shifts = load_shifts(shift_file)

    # Initialize calendar
    calendar = Calendar()
    local_timezone = pytz.timezone("Europe/Rome")  # Set your timezone

    # Process CSV
    with open(csv_file, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip header row
        for row in reader:
            event_name, date_str, shift_name = row

            # Parse shift times
            shift_times = shifts.get(shift_name)
            if not shift_times:
                print(f"Warning: Shift '{shift_name}' not found. Skipping event '{event_name}'.")
                continue

            start_time_str, end_time_str = shift_times.split(' - ')
            start_datetime = local_timezone.localize(datetime.strptime(f"{date_str} {start_time_str}", '%d/%m/%y %H:%M'))
            end_datetime = datetime.strptime(f"{date_str} {end_time_str}", '%d/%m/%y %H:%M')

            # Handle overnight shifts
            if end_datetime.time() < start_datetime.time():
                end_datetime += timedelta(days=1)

            end_datetime = local_timezone.localize(end_datetime)

            # Convert to UTC for Google Calendar
            start_datetime = start_datetime.astimezone(pytz.utc)
            end_datetime = end_datetime.astimezone(pytz.utc)

            # Create event
            event = Event()
            event.name = event_name
            event.begin = start_datetime
            event.end = end_datetime
            event.uid = f"{event_name}-{date_str}@example.com"  # Unique identifier
            event.created = datetime.now(pytz.utc)  # Add DTSTAMP

            # Add event to calendar
            calendar.events.add(event)

    # Write calendar to file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(calendar)

if __name__ == "__main__":
    # Filenames
    csv_filename = "events.csv"
    shift_filename = "shifts.json"
    output_filename = "calendar.ics"

    # Check files exist
    if not os.path.exists(csv_filename):
        print(f"Error: {csv_filename} not found.")
        exit(1)

    if not os.path.exists(shift_filename):
        print(f"Error: {shift_filename} not found.")
        exit(1)

    # Generate ICS file
    create_ics_from_csv(csv_filename, shift_filename, output_filename)
    print(f"ICS file generated: {output_filename}")