# AI Calendar Agent in Pure Python

The **AI Calendar Agent in Pure Python** is a console-based application designed to demonstrate fundamental agentic AI principles through a practical calendar management interface. This project allows users to interact with a personal calendar using natural language commands, showcasing how a rule-based agent can interpret requests, manage internal state, and execute defined "tools" or functions without relying on external AI/NLP libraries.

## Table of Contents

*   [Project Overview](#project-overview)
*   [Features](#features)
*   [Core Concepts](#core-concepts)
*   [Getting Started](#getting-started)
    *   [Prerequisites](#prerequisites)
    *   [Installation](#installation)
    *   [Running the Agent](#running-the-agent)
*   [Usage](#usage)
*   [Agent Architecture](#agent-architecture)
*   [Code Structure](#code-structure)
*   [Limitations and Future Enhancements](#limitations-and-future-enhancements)
*   [Contributing](#contributing)
*   [License](#license)

## Project Overview

This project implements a simple AI agent that functions as a calendar assistant. It processes natural language input to perform actions such as adding new events, viewing scheduled events for specific dates, and deleting existing events. The core focus is on building a self-contained, intelligent system using only Python's standard library, particularly regular expressions for natural language understanding (NLU) and standard data structures for state management.

The agent's decision-making process is rule-based, mapping user commands to predefined functions (tools) that manipulate the calendar's in-memory data. This provides a clear and educational example of an agent's perception-action loop.

## Features

*   **Natural Language Command Processing:** Understands specific patterns for adding, viewing, and deleting calendar events.
*   **Event Creation:** Add events with a title, date (YYYY-MM-DD, "today", "tomorrow"), and optional time (HH:MM).
*   **Event Viewing:**
    *   Display all upcoming events.
    *   Display events scheduled for a specific date.
*   **Event Deletion:** Remove events using their unique identifier.
*   **Help System:** Provides a list of available commands upon request.
*   **Pure Python Implementation:** No external dependencies beyond the standard library, making it lightweight and easy to inspect.

## Core Concepts

The project serves as an educational tool, illustrating several core concepts in agentic AI and software development:

*   **Agentic Design:** Demonstrates a basic agent architecture with a clear perception-action cycle, where the agent perceives user input, plans a response (interprets intent), and executes an action (calls a tool).
*   **Rule-Based AI:** Utilizes regular expressions and conditional logic to interpret natural language commands, providing a foundational understanding of NLU without complex machine learning models.
*   **Tool Use:** Emphasizes the concept of an AI agent interacting with a set of predefined "tools" (Python functions) to achieve its objectives.
*   **State Management:** Manages the calendar's events in an in-memory list, simulating how an agent maintains and updates its understanding of the environment.
*   **Modular Programming:** Separates concerns into distinct functions for parsing, event management, and agent logic, promoting code readability and maintainability.

## Getting Started

### Prerequisites

*   **Python 3.7+**: Ensure Python is installed and accessible via your system's PATH.

### Installation

No installation steps are required. Simply download or clone the repository and navigate to the project directory.

```bash
git clone https://github.com/your-username/ai-calendar-agent-python.git
cd ai-calendar-agent-python
```
*(Replace `your-username/ai-calendar-agent-python.git` with your actual repository URL)*

### Running the Agent

To start the AI Calendar Agent, execute the `calendar_agent.py` script from your terminal:

```bash
python calendar_agent.py
```

The agent will launch in your console, displaying a welcome message and a prompt for commands.

## Usage

Interact with the agent by typing commands at the `> Your command:` prompt.

**Available Commands:**

*   **Add an event:**
    *   `add <title> on <YYYY-MM-DD> [at <HH:MM>]`
        *   _Example:_ `add team meeting on 2024-01-15 at 10:00`
    *   `add <title> (today|tomorrow) [at <HH:MM>]`
        *   _Example:_ `add dentist appointment tomorrow at 14:30`
*   **View events for a specific date:**
    *   `view events on <YYYY-MM-DD>`
        *   _Example:_ `view events on 2024-01-15`
    *   `what's happening (today|tomorrow)`
        *   _Example:_ `what's happening today`
    *   `show me (today's|tomorrow's) schedule`
        *   _Example:_ `show me tomorrow's schedule`
*   **View all upcoming events:**
    *   `view all events`
    *   `show upcoming events`
    *   `show my schedule`
*   **Delete an event:**
    *   `delete event <ID>` (Event IDs are displayed when viewing events)
        *   _Example:_ `delete event 5`
*   **Help:**
    *   `help`
*   **Exit:**
    *   `exit`

**Example Interaction:**

```
Welcome to the AI Calendar Agent!
Type 'help' for a list of commands, or 'exit' to quit.

> Your command: add project kickoff on 2024-02-01 at 09:30
Event 'project kickoff' added for 2024-02-01 at 09:30.

> Your command: add design review today at 13:00
Event 'design review' added for 2024-01-15 at 13:00.

> Your command: view all events
Upcoming Events:
- [2024-01-15 13:00] design review
- [2024-02-01 09:30] project kickoff

> Your command: delete event 1
Event with ID 1 deleted.

> Your command: show my schedule
Upcoming Events:
- [2024-02-01 09:30] project kickoff

> Your command: exit
Goodbye!
```
*(Note: Dates in example interaction assume current date for "today" and "tomorrow" commands.)*

## Agent Architecture

The AI Calendar Agent's architecture is structured to facilitate clear separation of concerns, mimicking a basic agentic framework:

1.  **User Input (Perception):** The agent continuously listens for natural language commands from the user via the console.
2.  **Agent's Brain (`process_command` function):**
    *   **Intent Recognition:** Utilizes a series of regular expressions to match incoming commands against known patterns for actions (e.g., "add," "view," "delete").
    *   **Parameter Extraction:** Extracts key information (event title, date, time, event ID) from the command based on the matched pattern.
    *   **Tool Selection & Execution:** Based on the recognized intent and extracted parameters, the agent determines which "agentic tool" (calendar management function) is appropriate and invokes it.
3.  **Agentic Tools (Functions):**
    *   `add_event_to_calendar`: Creates and stores a new event.
    *   `view_events_on_date`: Retrieves events for a specified date.
    *   `view_all_upcoming_events`: Lists all future scheduled events.
    *   `delete_event_by_id`: Removes an event using its unique identifier.
    *   These tools interact directly with the `calendar_events` data structure.
4.  **Calendar Data (`calendar_events` list):** An in-memory list of dictionaries, representing the agent's internal model of the calendar state. Each dictionary contains event details (`id`, `title`, `date`, `time`).
5.  **Agent Response (Action):** The result from the executed tool is formatted into a user-friendly message and displayed in the console.

## Code Structure

*   `calendar_agent.py`:
    *   `calendar_events`: Global list representing the calendar's state.
    *   `parse_date(date_str)`: Helper for converting string dates to `datetime.date` objects.
    *   `parse_time(time_str)`: Helper for converting string times to `datetime.time` objects.
    *   `format_event(event)`: Helper for rendering event dictionaries into readable strings.
    *   `add_event_to_calendar(...)`: Agentic tool for adding events.
    *   `view_events_on_date(...)`: Agentic tool for viewing events on a specific date.
    *   `view_all_upcoming_events()`: Agentic tool for viewing all upcoming events.
    *   `delete_event_by_id(event_id)`: Agentic tool for deleting events.
    *   `process_command(command)`: The agent's core logic for intent parsing and tool orchestration.
    *   `run_agent()`: The main loop for user interaction.

## Limitations and Future Enhancements

As an introductory project, this AI Calendar Agent has several limitations and offers numerous avenues for expansion:

*   **Lack of Persistence:** All events are stored in memory and are lost when the program exits.
    *   **Enhancement:** Implement saving and loading events from a file (e.g., JSON, CSV) or a simple database (e.g., SQLite).
*   **Simple NLP:** Relies heavily on exact regular expression matches.
    *   **Enhancement:** Incorporate more advanced NLP techniques (e.g., fuzzy matching, entity recognition using libraries like SpaCy or NLTK) for greater flexibility in user input.
*   **No Context Retention:** Each command is processed independently.
    *   **Enhancement:** Implement basic dialogue management to handle follow-up questions or contextual references (e.g., "What about tomorrow?" after viewing today's events).
*   **No Conflict Resolution:** Does not check for overlapping events.
    *   **Enhancement:** Add logic to detect and notify the user of potential schedule conflicts.
*   **No Recurring Events:** Cannot handle events that repeat daily, weekly, etc.
    *   **Enhancement:** Introduce a mechanism for defining and managing recurring events.
*   **Basic Error Handling:** Error messages are functional but could be more user-friendly.
    *   **Enhancement:** Improve error feedback and guide users towards correct command structures.
*   **Time Zone Support:** All times are assumed to be in the local timezone.
    *   **Enhancement:** Add support for specifying and converting between time zones.

## Contributing

Contributions are welcome! If you have suggestions for improvements, bug fixes, or new features, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add <your-feature>'`).
5.  Push to the branch (`git push origin feature/your-feature`).
6.  Open a Pull Request.




