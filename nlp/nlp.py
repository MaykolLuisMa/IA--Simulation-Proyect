#dependencias
from openai import OpenAI
from nlp.prompt import *

#respuesta del modelo a la query ingresada por el usuario
def response(query: str):
  #cargar el server local
  client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

  completion = client.chat.completions.create(
    model="NousResearch/Hermes-2-Pro-Mistral-7B-GGUF",
    messages=[
      {"role": "system", "content": SYSTEM_PROMPT},
      {"role": "user", "content": build_prompt(query)}
    ],
    temperature=0.7,
  )
  
  return completion.choices[0].message.content
