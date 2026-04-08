from agents.gemini_base import run_gemini_agent
from tools.mcp_tools import NOTES_TOOLS
from tools.firestore_tools import create_note, list_notes, search_notes, update_note

TOOL_MAP = {
    "create_note": create_note,
    "list_notes": list_notes,
    "search_notes": search_notes,
    "update_note": update_note,
}

SYSTEM = """You are the Notes Agent for OmniDesk.

Help users capture ideas, search through notes, and organize information.

When listing or showing notes, ALWAYS format each note like this — use real line breaks:

📝 Note Title (or first line of note)
  Tags: #tag1 #tag2
  Created: 2025-04-08
  Content: The note content here...

Separate each note with a blank line.
Do NOT put everything on one line.
Do NOT use markdown ** or __.
Suggest relevant tags when creating notes.
"""


def format_notes(notes: list) -> str:
    if not notes:
        return "You have no notes yet. Want to capture something?"

    lines = ["Here are your notes:\n"]
    for n in notes:
        title = n.get("title") or n.get("content", "Untitled")[:40]
        lines.append(f"📝 {title}")
        if n.get("tags"):
            tags = " ".join(f"#{t}" for t in n["tags"])
            lines.append(f"  Tags: {tags}")
        if n.get("created_at"):
            lines.append(f"  Created: {n['created_at'][:10]}")
        content = n.get("content", "")
        if content and content != title:
            preview = content[:120] + ("..." if len(content) > 120 else "")
            lines.append(f"  {preview}")
        lines.append("")
    return "\n".join(lines)


def run_notes_agent(user_request: str) -> str:
    lower = user_request.lower()

    if any(kw in lower for kw in ["list", "show", "all notes", "my notes"]):
        result = list_notes()
        return format_notes(result.get("notes", []))

    return run_gemini_agent(SYSTEM, user_request, NOTES_TOOLS, TOOL_MAP)