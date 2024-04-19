#comportamiento del modelo
SYSTEM_PROMPT = "Eres un asistente que responde preguntas sobre sexo"

#prompt generado con la query del usuario
def build_prompt(query: str):
  prompt = f'Necesito que proceses la siguiente peticion de un usuario: {query}'
  return prompt