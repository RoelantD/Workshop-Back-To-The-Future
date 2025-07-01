import os
import random
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ToolSet,FunctionTool, AzureAISearchTool, AzureAISearchQueryType, MessageRole
from dotenv import load_dotenv

############################
# Create an AIProjectClient instance
############################

load_dotenv(override=True)

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_CONNECTION_STRING"],
    credential=DefaultAzureCredential()
)

with project_client:
    ############################
    # Function to predict which team will win
    ############################
    def predict_winner(home: str, away: str) -> str:
        """
        Predicts the winner of a match between two teams.

        :param home: The home team.
        :param away: The away team.
        :return: The predicted winner.
        """
        return random.choice([home, away])
    
    
    functions = FunctionTool(functions={predict_winner})

    ############################
    # Creating the toolset
    ############################
    toolset = ToolSet()
    toolset.add(functions)
    project_client.agents.enable_auto_function_calls(toolset)


    ############################I
    # Creating the agent
    ############################
    agent = project_client.agents.create_agent(
        model="gpt-4o",
        name="my-agent",
        instructions=open("part-2/code/instructions.txt").read(),
        toolset=toolset  # Add the toolset to the agent
    )
    print(f"Created agent, ID: {agent.id}")


    ############################
    # Create a thread for communication
    ############################
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        ############################
        # Add a message to the thread
        ############################
        message = project_client.agents.messages.create(
            thread_id=thread.id,
            role= MessageRole.USER, 
            content = user_input
        )
    
        # Create and process an agent run
        run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    
        # Fetch and log all messages
        messages = project_client.agents.messages.list(thread_id=thread.id)
        first_message = next(iter(messages), None)
        if first_message:
            # Print the 'value' from the first text message content
            print(next((item["text"]["value"] for item in first_message.content if item.get("type") == "text"), ""))
    

        
    #############################
    # Delete the agent when done
    #############################
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")