#comportamiento del modelo
SYSTEM_PROMPT = "Eres un asistente que recibe un texto y responde a peticiones relacionado con el mismo"

#prompt generado con la query del usuario
def build_prompt(query: str):
  prompt = 'Necesito que me envies un objeto de tipo json solamente con los cambos "name" y "age"\n'
  prompt += 'En dependencia de lo que ingrese el usuario procesa los datos y enviame el archivo json. Esta es la informacion del usuario:\n'
  prompt += f'"{query}"'
  return prompt