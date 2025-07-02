# sports2.py


import requests
import json
import os
import pandas as pd

# Set up the base URL for the local Ollama API
url = "http://localhost:11434/api/chat"



# Read the CSV file and prepare a summary for the model
csv_path = "local/england-premier-league-2019-to-2020.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV file not found: {csv_path}")

df = pd.read_csv(csv_path)


# Create a summary that explicitly links Home Team to Full Time Home Goals, and Away Team to Full Time Away Goals
if all(col in df.columns for col in ["HomeTeam", "FTHG", "AwayTeam", "FTAG"]):
    # Build a sample of match results
    match_samples = []
    for idx, row in df.head(5).iterrows():
        match_samples.append(f"{row['HomeTeam']} {int(row['FTHG'])} - {int(row['FTAG'])} {row['AwayTeam']}")
    match_sample_str = "\n".join(match_samples)
    summary = (
        "In this dataset, 'HomeTeam' is linked to 'FTHG' (Full Time Home Goals), and 'AwayTeam' is linked to 'FTAG' (Full Time Away Goals). "
        "Here are some sample results from the 2019-2020 season:\n" + match_sample_str
    )
else:
    summary = df.describe(include='all').to_string()


# Prepare a prompt for football match predictions for the upcoming season
prompt = (
    "You are the AI Sports Almanac from 'Back to the Future', specialized in football (soccer). "
    "Based on the English Premier League 2019-2020 data below, give your bold predictions for the upcoming 2020-2021 season. "
    "List the predicted champion, the full top 3, and at least three remarkable match results with scores. For each, add a fun Almanac-style fact. "
    "Do NOT return code or a Python script—just give your results and predictions as if you are the Almanac, in clear English prose.\n"
    f"Here is the summary of the 2019-2020 season:\n{summary}"
)

payload = {
    "model": "llama3.2",
    "messages": [
        {
            "role": "system",
            "content": "You are the AI Sports Almanac from 'Back to the Future', specialized in football (soccer). Always answer as the Almanac: confident, detailed, a bit cheeky, and with fun facts. Use the CSV data to support your predictions."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
}

# Send the HTTP POST request with streaming enabled
response = requests.post(url, json=payload, stream=True)

# Check the response status
if response.status_code == 200:
    print("Streaming response from Ollama:")
    for line in response.iter_lines(decode_unicode=True):
        if line:  # Ignore empty lines
            try:
                # Parse each line as a JSON object
                json_data = json.loads(line)
                # Extract and print the assistant's message content
                if "message" in json_data and "content" in json_data["message"]:
                    print(json_data["message"]["content"], end="")
            except json.JSONDecodeError:
                print(f"\nFailed to parse line: {line}")
    print()  # Ensure the final output ends with a newline
else:
    print(f"Error: {response.status_code}")
    print(response.text)
