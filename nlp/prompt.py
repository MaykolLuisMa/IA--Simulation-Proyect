#comportamiento del modelo
SYSTEM_PROMPT = "Eres un asistente que recibe un texto y responde a peticiones relacionado con el mismo"

#prompt generado con la query del usuario
def build_prompt(sim: str, query: str):
  prompt = 'Necesito que me envies un objeto de tipo json solamente con el campo "result".'
  prompt += 'Te voy a enviar una informacion relativa a una simulacion del funcionamiento de un sistema economico.'
  prompt = 'Esta es la informacion de la simulacion:\n'
  prompt += f'"{sim}".\n'
  prompt += 'A continuacion t voy a enviar una pregunta de un usuario relacionada con la simulacion que te acabo de enviar.'
  prompt += 'En dependencia de lo que ingrese el usuario procesa los datos y devuelveme la respuesta lo mas concreta y objetiva posible en el campo "result" del archivo .json.'
  prompt += 'Esta es la peticion del usuario:\n'
  prompt += f'"{query}"'
  return prompt