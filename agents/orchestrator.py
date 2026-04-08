import vertexai
from vertexai.generative_models import (
    GenerativeModel, Tool, FunctionDeclaration, Part
)
import json, os

from agents.task_agent import run_task_agent
from agents.calendar_agent import run_calendar_agent
from agents.notes_agent import run_notes_agent

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "omnidesk-ai")
REGION = os.environ.get("REGION", "us-central1")
vertexai.init(project=PROJECT_ID, location=REGION)

ORCHESTRATOR_TOOL_DEFS = [
    FunctionDeclaration(
        name="delegate_to_task_agent",
        description="Delegate to Task Agent for: creating tasks, listing todos, updating task status, setting priorities, deleting tasks.",
        parameters={
            "type": "object",
            "properties": {"request": {"type": "string", "description": "The task management request"}},
            "required": ["request"]
        }
    ),
    FunctionDeclaration(
        name="delegate_to_calendar_agent",
        description="Delegate to Calendar Agent for: scheduling meetings, creating events, viewing schedule, managing appointments.",
        parameters={
            "type": "object",
            "properties": {"request": {"type": "string", "description": "The scheduling request"}},
            "required": ["request"]
        }
    ),
    FunctionDeclaration(
        name="delegate_to_notes_agent",
        description="Delegate to Notes Agent for: capturing ideas, writing notes, searching information, organizing knowledge.",
        parameters={
            "type": "object",
            "properties": {"request": {"type": "string", "description": "The notes request"}},
            "required": ["request"]
        }
    )
]

AGENT_MAP = {
    "delegate_to_task_agent": run_task_agent,
    "delegate_to_calendar_agent": run_calendar_agent,
    "delegate_to_notes_agent": run_notes_agent,
}

SYSTEM = """You are OmniDesk, an intelligent personal AI chief of staff powered by Gemini.
You coordinate specialized agents to help users manage tasks, schedules, and information.

Your agents:
- Task Agent: todos, action items, priorities
- Calendar Agent: events, meetings, appointments
- Notes Agent: ideas, information, knowledge capture

For each user request:
1. Identify what type(s) of help are needed
2. Delegate to the right agent(s) — can use multiple for complex requests
3. For requests spanning multiple domains, coordinate agents in sequence
4. Synthesize results into a clear, friendly, useful response

Be proactive: if someone mentions a meeting, also offer to create a prep task."""

def run_orchestrator(user_message: str) -> dict:
    tools = [Tool(function_declarations=ORCHESTRATOR_TOOL_DEFS)]
    model = GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=SYSTEM,
        tools=tools
    )

    chat = model.start_chat()
    response = chat.send_message(user_message)
    execution_log = []

    for _ in range(8):
        fn_calls = []
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.function_call.name:
                    fn_calls.append(part.function_call)

        if not fn_calls:
            # Final text response
            for candidate in response.candidates:
                for part in candidate.content.parts:
                    if part.text:
                        return {"response": part.text, "agents_used": execution_log}
            return {"response": "Done.", "agents_used": execution_log}

        tool_response_parts = []
        for fn_call in fn_calls:
            fn_name = fn_call.name
            fn_args = dict(fn_call.args)
            agent_fn = AGENT_MAP.get(fn_name)

            label = fn_name.replace("delegate_to_", "").replace("_agent", "").title()
            execution_log.append({"agent": label, "request": fn_args.get("request", "")})

            result = agent_fn(fn_args["request"]) if agent_fn else "Agent not found"

            tool_response_parts.append(
                Part.from_function_response(
                    name=fn_name,
                    response={"result": result}
                )
            )

        response = chat.send_message(tool_response_parts)

    return {"response": "Completed.", "agents_used": execution_log}