# Adding an OpenAPI spec (**5_full_file_search.py**)

Now we're going to enhance our agent with the ability to call external APIs using OpenAPI specifications. This powerful feature allows our agent to interact with real-world services, making it more practical and capable of performing actual business operations.

In this step, we'll add an OpenAPI tool that enables our agent to:
- Retrieve current betting opportunities
- Place bets on football matches

## Understanding OpenAPI Tools

OpenAPI tools allow agents to call external REST APIs by providing a structured specification (swagger.json) that describes:
- Available endpoints
- Required parameters
- Request/response schemas
- Authentication methods

The agent uses this specification to understand how to make proper API calls when needed.

## The Swagger Specification

Let's first examine our **swagger.json** file that defines the betting API:

```json
{
  "openapi": "3.0.4",
  "info": {
    "title": "Cloudland.Workshop.Sports.API",
    "version": "1.0"
  },
  "servers": [
    {
      "url": "https://app-betting-api.azurewebsites.net/api",
      "description": "Production server"
    }
  ],
  "paths": {
    "/api/bet": {
      "post": {
        "operationId": "PlaceBet",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/BetRequest"
              }
            }
          }
        }
      }
    },
    "/api/betting-opportunity": {
      "get": {
        "operationId": "GetCurrentBettingOpportunity"
      }
    }
  }
}
```

This specification defines two key endpoints:
- **GET /api/betting-opportunity**: Retrieves current betting opportunities
- **POST /api/bet**: Places a bet with specific parameters

### Additional Imports

First, we need to import the necessary modules for OpenAPI functionality:

```python
import jsonref
from azure.ai.agents.models import OpenApiTool, OpenApiAnonymousAuthDetails
```

- `jsonref`: Handles JSON reference resolution in OpenAPI specs
- `OpenApiTool`: The tool class for OpenAPI integration
- `OpenApiAnonymousAuthDetails`: Handles authentication (anonymous in our case)

### Loading the OpenAPI Specification

We load and parse our swagger.json file:

```python
############################
# OpenApiTool
############################
with open(os.path.join(os.path.dirname(__file__), "/part-2/code/swagger.json"), "r") as f:
        openapi_betting_api = jsonref.loads(f.read())

openapi_tool = OpenApiTool(
    name="betting_api", 
    spec=openapi_betting_api, 
    description="Place bets, retrieve betting options, and check bet status", 
    auth=OpenApiAnonymousAuthDetails()
)
```

**Key components:**
- **name**: A unique identifier for this API tool
- **spec**: The parsed OpenAPI specification 
- **description**: Helps the agent understand when to use this tool
- **auth**: Authentication method (anonymous for this demo)

### Enhanced Toolset

Now our toolset includes three types of tools:

```python
############################
# Creating the toolset
############################
toolset = ToolSet()
toolset.add(file_search)      # Knowledge base search
toolset.add(openapi_tool)     # External API calls
toolset.add(functions)        # Custom Python functions
project_client.agents.enable_auto_function_calls(toolset)
```

This gives our agent a comprehensive set of capabilities:
1. **File search**: Query the knowledge base from documents
2. **OpenAPI tool**: Call external betting APIs
3. **Function tool**: Execute custom Python logic

## Testing Your Enhanced Agent

Start the **5_full_file_search.py** script and try these interactions:

### 1. Get Betting Opportunities
```
You: What betting opportunities are currently available?
```

The agent should call the `GetCurrentBettingOpportunity` endpoint and return the available matches.

### 2. Place a Bet
```
You: I want to place a bet on the next match. I think the home team will win.
```

The agent should:
1. First get current betting opportunities
2. Ask for additional details if needed (amount, user ID)
3. Call the `PlaceBet` endpoint with the proper parameters

### 3. Combined Intelligence
```
You: Based on the character knowledge and my prediction function, what would Biff Tannen bet on?
```

This tests the agent's ability to:
1. Search the knowledge base about Biff Tannen
2. Use the predict_winner function
3. Potentially place a bet via the API

## Understanding the Agent's Decision Making

The agent automatically decides which tools to use based on:
- **User intent**: What the user is asking for
- **Tool descriptions**: How each tool is described
- **Context**: Previous conversation and available data

For example:
- Questions about characters → File search tool
- Prediction requests → Function tool  
- Betting actions → OpenAPI tool
- Complex requests → Multiple tools in sequence

## Key Benefits of OpenAPI Integration

1. **Real-world connectivity**: Agent can interact with actual services
2. **Standardized interface**: OpenAPI specs provide clear contracts
3. **Automatic discovery**: Agent understands available operations from the spec
4. **Error handling**: Built-in validation and error responses
5. **Scalability**: Easy to add more APIs by providing additional specs

## Exercise: Enhance the Betting Logic

Try modifying the `predict_winner` function to:
1. Call your ML model endpoint from Part 1
2. Use the actual prediction to influence betting decisions
3. Consider the betting odds when making recommendations

This will create a more sophisticated agent that combines:
- Machine learning predictions
- Knowledge base information  
- Real API interactions
- Business logic

## Troubleshooting

**Common issues:**
- **File path errors**: Ensure swagger.json path is correct
- **API connectivity**: Check if the betting API endpoint is accessible
- **Authentication**: Verify OpenApiAnonymousAuthDetails() is appropriate
- **JSON parsing**: Validate your swagger.json is properly formatted

Your agent now has the full spectrum of capabilities - from knowledge retrieval to API integration to custom business logic!

[⏮️ Previous](/part-2/2-4-add-tools.md)