from agents.gemini_base import run_gemini_agent
from tools.mcp_tools import TASK_TOOLS
from tools.firestore_tools import create_task, list_tasks, update_task, delete_task

TOOL_MAP = {
    "create_task": create_task,
    "list_tasks": list_tasks,
    "update_task": update_task,
    "delete_task": delete_task,
}

SYSTEM = """You are the Task Management Agent for OmniDesk.

Help users create, list, update, and delete tasks.

When listing or showing tasks, ALWAYS format each task exactly like this — use real line breaks between each field:

• Task Title
  Priority: High
  Due: 2025-04-15
  Status: Pending

Separate each task with a blank line.
Do NOT put everything on one line.
Do NOT use markdown ** or __ for bold.
Do NOT use dashes - at the start of lines.
Use the bullet character • for each task title only.
"""


def format_tasks(tasks: list) -> str:
    """Formats a list of task dicts into clean bullet output."""
    if not tasks:
        return "You have no tasks yet. Try asking me to create one!"

    lines = ["Here are your tasks:\n"]
    for t in tasks:
        lines.append(f"• {t['title']}")
        lines.append(f"  Priority: {t.get('priority', 'normal').capitalize()}")
        lines.append(f"  Due: {t.get('due_date', 'N/A')}")
        lines.append(f"  Status: {t.get('status', 'pending').capitalize()}")
        lines.append("")  # blank line between tasks
    return "\n".join(lines)


def run_task_agent(user_request: str) -> str:
    lower = user_request.lower()

    # For list/show queries: fetch directly and format ourselves
    if any(kw in lower for kw in ["list", "show", "what tasks", "my tasks", "all tasks", "pending"]):
        result = list_tasks()
        return format_tasks(result.get("tasks", []))

    # For create/update/delete: use Gemini then re-format if it returns tasks
    response = run_gemini_agent(SYSTEM, user_request, TASK_TOOLS, TOOL_MAP)
    return response