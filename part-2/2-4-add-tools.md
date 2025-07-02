# Adding a function tool call (**4_function_call.py**)

Our agent now has the ability to be infused with our own data, but the real power with agents lies in the ability to create a detailed plan, work through it, and check status along the way.

Agents are able to call tools and functions we give it to provide business logic, API calls, or every conceivable Python code for that matter. 

We are going to add this function for the agent to call

```
def predict_winner(home: str, away: str) -> str:
    """
    Predicts the winner of a match between two teams.

    :param home: The home team.
    :param away: The away team.
    :return: The predicted winner.
    """
    return random.choice([home, away])
```

The general and parameter descriptions help the agent to figure out when to call this function and what parameters it needs to execute the function. If it needs more data it should ask the user (as that is in its [instructions.txt](code/instructions.txt))

We add these functions to the agent toolset by

```
functions = FunctionTool(functions={predict_winner})
```

Start the **4_function_calling.py** and ask it *Can you predict a winner?*

It should request more data from you and execute the function to randomly pick the home or away team.

## Update the predict_winner function to leverage your ML model
Now it is time to add some logic to consume your ML model you created in [part 1](/part-1/README.md).

Implement the API call and call the prediction endpoint to get a prediction from the model.

[⏮️ Previous](/part-2/2-3-add-knowledge.md) 
[⏭️ Next](/part-2/2-5-add-openapi.md)