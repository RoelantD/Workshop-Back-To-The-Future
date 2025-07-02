# Running a Local LLM Model via Ollama

This folder demonstrates how to install and run a local LLM using [Ollama](https://ollama.com), with example payloads and Python integrations.

## Contents

- `sports1.py`: Basic example showing how to integrate with the Ollama module. 
- `sports2.py`: Example using a general-purpose model.
- `sports3.py`: Demonstrates consuming a locally running Ollama model via an API, including usage of a custom model.

---

## Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com) installed  
  Install via pip:  
  ```bash
  pip install ollama
  ```

- Run Ollama with a model (e.g., LLaMA 3.2):  
  ```bash
  ollama run llama3.2
  ```

- [Pandas](https://pandas.pydata.org/) installed:
  ```bash
  pip install pandas
  ```

- A dataset (see below)

---

## Get a Sports Dataset

You can download sports datasets from:  
👉 [https://sports-statistics.com/sports-data/soccer-datasets/](https://sports-statistics.com/sports-data/soccer-datasets/)

---

## Creating Your Own Ollama Model

You can create a custom model using a modelfile:

```bash
ollama create almanac -f ./modelfile
```