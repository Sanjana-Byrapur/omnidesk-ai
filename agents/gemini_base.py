import vertexai
from vertexai.generative_models import (
    GenerativeModel, Tool, FunctionDeclaration, Part, Content
)
import json
import os

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "omnidesk-ai")
REGION = os.environ.get("REGION", "us-central1")

vertexai.init(project=PROJECT_ID, location=REGION)

def build_gemini_tools(tool_defs: list) -> list:
    """Convert our tool dicts to Gemini FunctionDeclaration objects."""
    declarations = []
    for t in tool_defs:
        declarations.append(FunctionDeclaration(
            name=t["name"],
            description=t["description"],
            parameters=t["parameters"]
        ))
    return [Tool(function_declarations=declarations)]

def run_gemini_agent(system_prompt: str, user_request: str,
                     tool_defs: list, tool_map: dict) -> str:
    """
    Generic Gemini agent loop with tool calling.
    Handles multi-turn tool use until model returns a final text response.
    """
    tools = build_gemini_tools(tool_defs)
    model = GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_prompt,
        tools=tools
    )

    chat = model.start_chat()
    response = chat.send_message(user_request)

    # Agentic loop — keep going while model wants to call tools
    for _ in range(10):  # max 10 iterations
        # Check for function calls
        fn_calls = []
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.function_call.name:
                    fn_calls.append(part.function_call)

        if not fn_calls:
            # No more tool calls — extract text response
            for candidate in response.candidates:
                for part in candidate.content.parts:
                    if part.text:
                        return part.text
            return "Done."

        # Execute all tool calls and collect results
        tool_response_parts = []
        for fn_call in fn_calls:
            fn_name = fn_call.name
            fn_args = dict(fn_call.args)

            tool_fn = tool_map.get(fn_name)
            if tool_fn:
                try:
                    result = tool_fn(**fn_args)
                except Exception as e:
                    result = {"error": str(e)}
            else:
                result = {"error": f"Unknown tool: {fn_name}"}

            tool_response_parts.append(
                Part.from_function_response(
                    name=fn_name,
                    response={"result": json.dumps(result)}
                )
            )

        # Send tool results back to model
        response = chat.send_message(tool_response_parts)

    return "Agent reached max iterations."