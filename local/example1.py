
from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': (
        'Why is the sky blue? '
        '(explain in one sentence, '
        'but make it sound like a 21th century scientist who is also a bit cheeky)'
    ),
  },
])
print(response['message']['content'])
