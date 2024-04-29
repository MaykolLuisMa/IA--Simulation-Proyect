#dependencias
from openai import OpenAI
from nlp.prompt import *
import json

#respuesta del modelo a la query ingresada por el usuario
def response(sim: str, query: str) -> str:
  #cargar el server local
  client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

  completion = client.chat.completions.create(
    model="NousResearch/Hermes-2-Pro-Mistral-7B-GGUF",
    messages=[
      {"role": "system", "content": SYSTEM_PROMPT},
      {"role": "user", "content": build_prompt(sim, query)}
    ],
    temperature=0.7,
  )
  
  json_result = completion.choices[0].message.content #respuesta en formato json
  result = json.loads(json_result) #parsear de json a dict
  return result['result']
