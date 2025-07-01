# Adding a vector store (**3_file_search.py**)

Up till now our agent was mainly a chatbot. A vanilla LLM we could steer in the right directions with some instructions. Every time we asked about Doc Browns birthdate it would hallucinate or say it would not know.

What if we could add the knowledge to our agent and make this knowledge base searchable by meaning, by adding it to a vector store. Vector stores are special datastores that store semantic meaning and similarity with references to the original files (or parts of these files).

First we create a vector store and upload some markdown documents in the [documents](/documents/) folder. This folder contains 5 markdown files on Back to the Future™️ characters, among which Doc Brown. Check out the file and note Docs birthdate is in there.

These lines creates a vector store and uploads the markdown documents so they can be processed.

```
file_ids = [
    project_client.agents.files.upload_and_poll(file_path=os.path.join("./documents", f), purpose=FilePurpose.AGENTS).id
    for f in os.listdir("./documents")
    if os.path.isfile(os.path.join("./documents", f))
]
```

Then we check if the vector store is ready and assign that to the variable

```
vector_store = project_client.agents.vector_stores.create_and_poll(data_sources=[], name="back-to-the-future-information")
```

We then vectorize the files and add them to the vector store

```
batch = project_client.agents.vector_store_file_batches.create_and_poll(
    vector_store_id=vector_store.id,
    file_ids=file_ids
)
```

And we create a tool for the file search

```
file_search = FileSearchTool(vector_store_ids=[vector_store.id])

toolset = ToolSet()
toolset.add(file_search)
```

We then add that tool to the agent toolset when creating the agent

```
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="my-agent",
    instructions=open("part-2/code/instructions.txt").read(),
    toolset=toolset  # Add the toolset to the agent
)
```

Run the Python file, and if we now ask for Doc Browns birthdate, it should be able to reproduce *January 14, 1914* without a problem.