import csv
import os
from datetime import datetime, timedelta
import json
import pytz
from ics import Calendar, Event

def load_shifts(shift_file):
    """Load shifts from a JSON file."""
    with open(shift_file, 'r', encoding='utf-8') as file:
        return json.load(file)

def create_ics_from_csv(csv_file, shift_file, output_file):
    """Generate an ICS file compatible with iPhone Calendar."""
    shifts = load_shifts(shift_file)
    calendar = Calendar()
    local_timezone = pytz.timezone("Europe/Rome")

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip header
        for row in reader:
            if len(row) < 3:
                continue
            event_name, date_str, shift_name = row

            shift_times = shifts.get(shift_name)
            if not shift_times:
                print(f"⚠ Shift '{shift_name}' not found. Skipping '{event_name}'.")
                continue

            start_time_str, end_time_str = shift_times.split(' - ')
            start_datetime = local_timezone.localize(
                datetime.strptime(f"{date_str} {start_time_str}", '%d/%m/%y %H:%M')
            )
            end_datetime = local_timezone.localize(
                datetime.strptime(f"{date_str} {end_time_str}", '%d/%m/%y %H:%M')
            )

            # Overnight shift handling
            if end_datetime <= start_datetime:
                end_datetime += timedelta(days=1)

            event = Event()
            event.name = event_name
            event.begin = start_datetime
            event.end = end_datetime
            event.uid = f"{event_name}-{date_str}-{shift_name}@mycalendar.local"
            event.created = datetime.now(local_timezone)
            event.dtstamp = datetime.now(local_timezone)

            calendar.events.add(event)

    # For iOS compatibility, ensure UTF-8 without BOM
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(calendar)

    print(f"✅ ICS file generated: {output_file}")

if __name__ == "__main__":
    csv_filename = "events.csv"
    shift_filename = "shifts.json"
    output_filename = "calendar.ics"

    if not os.path.exists(csv_filename):
        print(f"❌ Error: {csv_filename} not found.")
        exit(1)
    if not os.path.exists(shift_filename):
        print(f"❌ Error: {shift_filename} not found.")
        exit(1)

    create_ics_from_csv(csv_filename, shift_filename, output_filename)
