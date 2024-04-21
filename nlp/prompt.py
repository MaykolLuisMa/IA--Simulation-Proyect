#comportamiento del modelo
SYSTEM_PROMPT = "Eres un asistente que recibe un texto y responde a peticiones relacionado con el mismo"

#prompt generado con la query del usuario
def build_prompt(query: str):
  prompt = 'Necesito que me envies un objeto de tipo json solamente con el campo "result"\n'
  prompt += 'En dependencia de lo que ingrese el usuario procesa los datos y almacena un resumen del procesamiento de la peticion.\n'
  prompt += 'Esta es la peticion del usuario:\n'
  prompt += f'"{query}"'
  return prompt