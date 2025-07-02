import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ToolSet,FilePurpose, FileSearchTool, MessageRole
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

def log_run_steps_and_tool_calls(project_client, thread, run):
    with open(f"logs/thread_{thread.id}_log.txt", "a") as log_file:
        run_steps = project_client.agents.run_steps.list(thread_id=thread.id, run_id=run.id)
        for step in run_steps:
            log_file.write(f"Step {step['id']} status: {step['status']}\n")
            step_details = step.get("step_details", {})
            tool_calls = step_details.get("tool_calls", [])

            if tool_calls:
                log_file.write("  Tool calls:\n")
                for call in tool_calls:
                    log_file.write(f"    Tool Call ID: {call.get('id')}\n")
                    log_file.write(f"    Type: {call.get('type')}\n")

                    azure_ai_search_details = call.get("azure_ai_search", {})
                    if azure_ai_search_details:
                        log_file.write(f"    azure_ai_search input: {azure_ai_search_details.get('input')}\n")
                        log_file.write(f"    azure_ai_search output: {azure_ai_search_details.get('output')}\n\n")

                    function_details = call.get("function", {})
                    if function_details:
                        log_file.write(f"    Function name: {function_details.get('name')}")
                        log_file.write(f"    Function output: {function_details.get('output')}\n\n")                    

                    file_search_details = call.get("file_search", {})
                    if file_search_details:
                        log_file.write(f"    File search output: {file_search_details.get('results')}\n\n")
                     