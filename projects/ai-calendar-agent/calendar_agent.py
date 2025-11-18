import re
import datetime

# --- Calendar Data Structure ---
# Simple in-memory calendar. .... but this could be a database.
calendar_events = []

# --- Helper Functions ---

def parse_date(date_str):
    """
    Attempts to parse a date string into a datetime.date object.
    Supports 'tomorrow', 'today', and YYYY-MM-DD format.
    """
    date_str = date_str.lower()
    if date_str == "today":
        return datetime.date.today()
    elif date_str == "tomorrow":
        return datetime.date.today() + datetime.timedelta(days=1)
    else:
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return None

def parse_time(time_str):
    """
    Attempts to parse a time string into a datetime.time object.
    Supports HH:MM format (24-hour).
    """
    try:
        return datetime.datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        return None

def format_event(event):
    """
    Formats an event dictionary into a human-readable string.
    """
    date_str = event['date'].strftime('%Y-%m-%d')
    time_str = event['time'].strftime('%H:%M') if event['time'] else "All Day"
    return f"[{date_str} {time_str}] {event['title']}"

# --- Agentic Functions (Tools) ---

def add_event_to_calendar(title, date_obj, time_obj=None):
    """
    Adds a new event to the calendar_events list.
    """
    event = {
        "id": len(calendar_events) + 1, # Simple ID generation
        "title": title,
        "date": date_obj,
        "time": time_obj
    }
    calendar_events.append(event)
    time_str = f" at {time_obj.strftime('%H:%M')}" if time_obj else ""
    return f"Event '{title}' added for {date_obj.strftime('%Y-%m-%d')}{time_str}."

def view_events_on_date(date_obj):
    """
    Retrieves and formats events for a specific date.
    """
    events_on_date = [e for e in calendar_events if e['date'] == date_obj]
    if not events_on_date:
        return f"No events found for {date_obj.strftime('%Y-%m-%d')}."
    
    response = f"Events for {date_obj.strftime('%Y-%m-%d')}:\n"
    for event in sorted(events_on_date, key=lambda x: x['time'] if x['time'] else datetime.time.min):
        response += f"- {format_event(event)}\n"
    return response.strip()

def view_all_upcoming_events():
    """
    Retrieves and formats all upcoming events.
    """
    today = datetime.date.today()
    upcoming_events = [e for e in calendar_events if e['date'] >= today]
    
    if not upcoming_events:
        return "No upcoming events."

    response = "Upcoming Events:\n"
    # Sort by date, then by time
    for event in sorted(upcoming_events, key=lambda x: (x['date'], x['time'] if x['time'] else datetime.time.min)):
        response += f"- {format_event(event)}\n"
    return response.strip()

def delete_event_by_id(event_id):
    """
    Deletes an event by its ID.
    """
    global calendar_events # Needed to modify the global list
    initial_len = len(calendar_events)
    calendar_events = [e for e in calendar_events if e['id'] != event_id]
    
    if len(calendar_events) < initial_len:
        return f"Event with ID {event_id} deleted."
    else:
        return f"No event found with ID {event_id}."

# --- Agent's Brain (Intent Parser and Executor) ---

def process_command(command):
    """
    The core agent logic: parses the command and calls the appropriate tool.
    """
    command = command.strip()  # Remove leading/trailing spaces

    # 1. Add Event
    add_pattern = re.compile(
        r"add\s+(?P<title>.+?)\s*(?:on|for)?\s*(?P<date>\d{4}-\d{2}-\d{2}|today|tomorrow)"
        r"(?:\s+at\s+(?P<time>\d{1,2}:\d{2}))?$",
        re.IGNORECASE
    )
    match = add_pattern.fullmatch(command)
    if match:
        title = match.group('title').strip()
        date_str = match.group('date')
        time_str = match.group('time')

        date_obj = parse_date(date_str)
        time_obj = parse_time(time_str) if time_str else None

        if date_obj:
            return add_event_to_calendar(title, date_obj, time_obj)
        else:
            return "Could not understand the date. Please use YYYY-MM-DD, 'today', or 'tomorrow'."

    # 2. View Events for a Specific Date
    # e.g., "view events on 2023-12-25"
    # e.g., "what's happening today"
    # e.g., "show me tomorrow's schedule"
    view_date_pattern = re.compile(
        r"(view|show|what's happening)\s+(events\s+(?:on\s+|for\s+)?|schedule\s+)?(?P<date>\d{4}-\d{2}-\d{2}|today|tomorrow)",
        re.IGNORECASE
    )
    match = view_date_pattern.match(command)
    if match:
        date_str = match.group('date')
        date_obj = parse_date(date_str)
        if date_obj:
            return view_events_on_date(date_obj)
        else:
            return "Could not understand the date. Please use YYYY-MM-DD, 'today', or 'tomorrow'."

    # 3. View All Upcoming Events
    # e.g., "view all events"
    # e.g., "show upcoming schedule"
    if "view all events" in command or "show upcoming events" in command or "show my schedule" in command:
        return view_all_upcoming_events()

    # 4. Delete Event by ID
    # e.g., "delete event 5"
    delete_pattern = re.compile(r"delete\s+event\s+(?P<id>\d+)$")
    match = delete_pattern.match(command)
    if match:
        event_id = int(match.group('id'))
        return delete_event_by_id(event_id)

    # 5. Help
    if command in ("help", "hi", "hello"):
        return (
            "Hello! I am your AI Calendar Agent.\n"
            "Here are the commands you can use:\n"
            "- Add an event: `add <title> on <YYYY-MM-DD> [at <HH:MM>]` (e.g., `add meeting on 2023-12-25 at 10:00`)\n"
            "- Add an event for today/tomorrow: `add <title> today [at <HH:MM>]` (e.g., `add dentist appointment tomorrow at 14:30`)\n"
            "- View events for a date: `view events on <YYYY-MM-DD>` or `what's happening today`\n"
            "- View all upcoming events: `view all events` or `show my schedule`\n"
            "- Delete an event: `delete event <ID>` (You'll see IDs when viewing events)\n"
            "- Type 'exit' to quit."
        )

    # If no command matches
    return "I didn't understand that command. Type 'help' for available commands."

# --- Main Agent Loop ---

def run_agent():
    """
    The main loop where the agent interacts with the user.
    """
    print("Welcome to the AI Calendar Agent!")
    print("Type 'help' for a list of commands, or 'exit' to quit.")
    
    while True:
        user_input = input("\n> Your command: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        response = process_command(user_input)
        print(response)

if __name__ == "__main__":
    run_agent()   # python calendar_agent.py

# Test with:

# help
# add meeting on 2025-12-14 at 10:00
# add meeting 2025-12-14 at 10:00
# add meeting for 2025-12-14 at 10:00
# add meeting today
# add meeting tomorrow at 09:00   
# add appointment on 2025-12-15 at 14:30
# view all events
# view events on 2025-12-14
# what's happening today
# what's happening tomorrow
# delete event 1
# delete event 99
# exit