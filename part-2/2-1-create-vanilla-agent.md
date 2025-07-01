# Create an agent to consume the ML endpoint

## Deploy Azure AI Foundry resource

We need to deploy an **Azure AI Foundry** resource in our resource group and deploy a gpt4-o base model.

1. Go to the [Azure Portal](https://portal.azure.com)

2. Select **Create a resource**

3. Search for **Foundry**

4. Create an **Azure AI Foundry** resource

5. Select your resource group

6. Give it a name following the format *aif-[firstname]-[lastname]*

7. Choose **Sweden Central** as the region

8. Keep clicking on **Next** until you hit the **Review + submit** tab

9. Click **Create**

## Deploy GPT4-o base model

1. Navigate to the created **Azure AI Foundry** resource

2. Click the **Go to Azure AI Foundry portal** button

3. Copy the **Azure AI Foundry project endpoint** and paste it in the **.env** file in the **part-2/code** folder.

4. In the Azure portal, click **Models + endpoint** in the left menu under **Assets**

5. Click the blue **+ Deploy model** button and select **Deploy base model**

6. Make sure the filter is set to **Chat completion**

7. Select the **gpt4-o** model and click **Confirm**

## Complete the .env file parameters
If there is only a .env.sample file, rename that file to .env. These are the environment variables our scripts use.

You should have already pasted in the project connection string from the Azure AI Foundry instance. 

You can leave the values in place, or adjust accordingly if you know what you are doing.

## Azure AI Foundry Agent Service

It is time to explore some Python code for creating our first agent. We are going to start with a vanilla agent (**1_model.py**) and work our way up to adding an OpenAPI spec for the agent to call (**5_full_file_search.py**). Every step adding more and more tools that set apart the agent from a regular LLM.

### Vanilla agent (**1_model.py**)
This is our starting point to get acquainted with Azure AI Foundry Agent Service.

These first couple of lines do the necessary imports and load in our environment variables in the .env file.

```
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import MessageRole
from dotenv import load_dotenv

############################
# Create an AIProjectClient instance
############################

load_dotenv(override=True)
```

We then create the model client to interact with our Azure AI Foundry instance

```
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_CONNECTION_STRING"],
    credential=DefaultAzureCredential()
)
```

We are using CLI credentials, so make sure you are [logged in](/log-in-cli.md) through the terminal.

With our project_client we can now create our agent instance. We tell it what model deployment to use, give it some instructions, give it a name, and some language model parameters.

```
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="my-agent",
    instructions="I'm a bot and I don't know anything.",
    top_p=0.7,
    temperature=0.7,
    )
```

Then create a thread. A thread is the container of all chat messages, so both the messages from the user as the agent.

```
thread = project_client.agents.threads.create()
```

In a never ending loop, we chat with the user by getting its question or response, querying the agent and presenting the user with the result

```
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
```

It is now time to run the Python script (make sure you have Python 3.11 or higher installed and have installed the requirements in the requirements.txt).
You can now interact with the agent in the terminal. Play around, but also ask about football and the birthdate of Doc Brown.

Since the LLM has no knowledge of the fictional character Doc Brown, it should respond with a hallucinated value or with a response it does not possess that knowledge.

[⏮️ Previous](/part-1/1-10-deploy-model.md) 
[⏭️ Next](/part-2/2-2-create-instructions.md)