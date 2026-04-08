from google.cloud import firestore
from datetime import datetime
import uuid

db = firestore.Client()

# ── TASKS ──────────────────────────────────────────────
def create_task(title: str, description: str = "", priority: str = "medium", due_date: str = "") -> dict:
    task_id = str(uuid.uuid4())[:8]
    task = {
        "id": task_id, "title": title, "description": description,
        "priority": priority, "due_date": due_date,
        "status": "pending", "created_at": datetime.utcnow().isoformat()
    }
    db.collection("tasks").document(task_id).set(task)
    return {"success": True, "task": task}

def list_tasks(status: str = None) -> dict:
    ref = db.collection("tasks")
    if status:
        ref = ref.where("status", "==", status)
    tasks = [doc.to_dict() for doc in ref.stream()]
    return {"tasks": tasks, "count": len(tasks)}

# def update_task(task_id: str, updates: dict) -> dict:
#     db.collection("tasks").document(task_id).update(updates)
#     return {"success": True, "task_id": task_id, "updates": updates}
def update_task(title: str, status: str):
    tasks_ref = db.collection("tasks")
    docs = tasks_ref.stream()

    for doc in docs:
        data = doc.to_dict()

        if data.get("title", "").lower() == title.lower():
            tasks_ref.document(doc.id).update({
                "status": status.lower()
            })
            return {"success": True, "title": title, "status": status}

    return {"success": False, "error": "Task not found"}

def delete_task(task_id: str) -> dict:
    db.collection("tasks").document(task_id).delete()
    return {"success": True, "task_id": task_id}

# ── EVENTS ─────────────────────────────────────────────
def create_event(title: str, date: str, time: str = "", description: str = "", duration_mins: int = 60) -> dict:
    event_id = str(uuid.uuid4())[:8]
    event = {
        "id": event_id, "title": title, "date": date,
        "time": time, "description": description,
        "duration_mins": duration_mins, "created_at": datetime.utcnow().isoformat()
    }
    db.collection("events").document(event_id).set(event)
    return {"success": True, "event": event}

def list_events(date: str = None) -> dict:
    ref = db.collection("events")
    if date:
        ref = ref.where("date", "==", date)
    events = [doc.to_dict() for doc in ref.stream()]
    events.sort(key=lambda x: (x.get("date", ""), x.get("time", "")))
    return {"events": events, "count": len(events)}

def delete_event(title: str) -> dict:
    try:
        docs = db.collection("events").stream()

        for doc in docs:
            if doc.to_dict().get("title", "").lower() == title.lower():
                db.collection("events").document(doc.id).delete()
                return {"success": True}

        return {"success": False, "error": "Event not found"}

    except Exception as e:
        return {"success": False, "error": str(e)}

# ── NOTES ──────────────────────────────────────────────
def create_note(title: str, content: str, tags: list = None) -> dict:
    note_id = str(uuid.uuid4())[:8]
    note = {
        "id": note_id, "title": title, "content": content,
        "tags": tags or [], "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    db.collection("notes").document(note_id).set(note)
    return {"success": True, "note": note}

def list_notes(tag: str = None) -> dict:
    notes = [doc.to_dict() for doc in db.collection("notes").stream()]
    if tag:
        notes = [n for n in notes if tag in n.get("tags", [])]
    return {"notes": notes, "count": len(notes)}

def search_notes(query: str) -> dict:
    notes = [doc.to_dict() for doc in db.collection("notes").stream()]
    results = [n for n in notes if query.lower() in n.get("content", "").lower()
               or query.lower() in n.get("title", "").lower()]
    return {"notes": results, "count": len(results)}

def update_note(note_id: str, content: str = None, title: str = None) -> dict:
    updates = {"updated_at": datetime.utcnow().isoformat()}
    if content: updates["content"] = content
    if title: updates["title"] = title
    db.collection("notes").document(note_id).update(updates)
    return {"success": True, "note_id": note_id}