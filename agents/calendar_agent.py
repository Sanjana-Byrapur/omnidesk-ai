from agents.gemini_base import run_gemini_agent
from tools.mcp_tools import CALENDAR_TOOLS
from tools.firestore_tools import create_event, list_events,delete_event

TOOL_MAP = {
    "create_event": create_event,
    "list_events": list_events,
    # "update_event": update_event,
    "delete_event": delete_event,
}

SYSTEM = """You are the Calendar Agent for OmniDesk.

Help users schedule meetings, create events, and view their calendar.

When listing or showing events, ALWAYS format each event exactly like this — use real line breaks:

📅 Event Title
  Date: 2025-04-10
  Time: 9:00 AM
  Duration: 30 minutes
  Location: (if provided)

Separate each event with a blank line.
Do NOT put everything on one line.
Do NOT use markdown ** or __.
"""


def format_events(events: list) -> str:
    if not events:
        return "You have no upcoming events. Want me to schedule something?"

    lines = ["Here are your upcoming events:\n"]
    for e in events:
        lines.append(f"📅 {e['title']}")
        lines.append(f"  Date: {e.get('date', 'N/A')}")
        lines.append(f"  Time: {e.get('time', 'N/A')}")
        if e.get("duration"):
            lines.append(f"  Duration: {e['duration']} minutes")
        if e.get("location"):
            lines.append(f"  Location: {e['location']}")
        lines.append("")
    return "\n".join(lines)


def run_calendar_agent(user_request: str) -> str:
    lower = user_request.lower()

    if any(kw in lower for kw in ["list", "show", "my events", "upcoming", "schedule", "what's on"]):
        result = list_events()
        return format_events(result.get("events", []))

    return run_gemini_agent(SYSTEM, user_request, CALENDAR_TOOLS, TOOL_MAP)