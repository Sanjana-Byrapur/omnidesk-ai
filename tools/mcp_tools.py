# Gemini-compatible tool (function) definitions

# ── TASK TOOLS ─────────────────────────────────────────

TASK_TOOLS = [
    {
        "name": "create_task",
        "description": "Create a new task",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Task title"},
                "description": {"type": "string", "description": "Task details"},
                "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                "due_date": {"type": "string", "description": "Due date YYYY-MM-DD"}
            },
            "required": ["title"]
        }
    },
    {
        "name": "list_tasks",
        "description": "List all tasks, optionally filtered by status",
        "parameters": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["pending", "completed"]}
            }
        }
    },
    {
        "name": "update_task",
        "description": "Update a task status using its title",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Task title"},
                "status": {"type": "string", "enum": ["pending", "completed"]}
            },
            "required": ["title", "status"]
        }
    },
    {
        "name": "delete_task",
        "description": "Delete a task using its title",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Task title"}
            },
            "required": ["title"]
        }
    }
]


# ── CALENDAR TOOLS ─────────────────────────────────────

CALENDAR_TOOLS = [
    {
        "name": "create_event",
        "description": "Create a calendar event",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "date": {"type": "string", "description": "YYYY-MM-DD"},
                "time": {"type": "string", "description": "HH:MM"},
                "description": {"type": "string"},
                "duration_mins": {"type": "integer"}
            },
            "required": ["title", "date"]
        }
    },
    {
        "name": "list_events",
        "description": "List calendar events",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "description": "Filter by YYYY-MM-DD"}
            }
        }
    },
    {
    "name": "delete_event",
    "description": "Delete a calendar event by its title",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {"type": "string"}
        },
        "required": ["title"]
    }
}
]


# ── NOTES TOOLS ────────────────────────────────────────

NOTES_TOOLS = [
    {
        "name": "create_note",
        "description": "Create a note",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "content": {"type": "string"},
                "tags": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["title", "content"]
        }
    },
    {
        "name": "list_notes",
        "description": "List all notes, optionally filtered by tag",
        "parameters": {
            "type": "object",
            "properties": {
                "tag": {"type": "string"}
            }
        }
    },
    {
        "name": "search_notes",
        "description": "Search notes by keyword",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "update_note",
        "description": "Update a note using its title",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Existing note title"},
                "new_title": {"type": "string", "description": "New title (optional)"},
                "content": {"type": "string", "description": "Updated content"}
            },
            "required": ["title"]
        }
    }
]