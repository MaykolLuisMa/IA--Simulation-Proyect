#comportamiento del modelo
SYSTEM_PROMPT = "Eres un asistente que recibe un texto y responde a peticiones relacionado con el mismo"

#prompt generado con la query del usuario
def build_prompt(sim: str, query: str):
  prompt = 'Necesito que me envies un objeto de tipo json solamente con el campo "result", es importante que no haya mas campos en el json, solo "result"'
  prompt += 'Te voy a enviar una informacion relativa a una simulacion del funcionamiento de un sistema economico y luego una consulta de un usuario.'
  prompt = 'Esta es la informacion de la simulacion:\n'
  prompt += f'"{sim}".\n'
  prompt += 'En dependencia de lo que ingrese el usuario procesa los datos de la simulacion y devuelveme la respuesta resumida en el campo "result" del archivo .json como te mencione anteriormente.'
  prompt += 'A continuacion t voy a enviar la consulta del usuario relacionada con la simulacion que te acabo de enviar.'
  prompt += 'Esta es la peticion del usuario:\n'
  prompt += f'"{query}"'
  return prompt

#prompt generado para el ruling
def rules_prompt(rules: str):
  prompt = 'Necesito que me envies un objeto de tipo json solamente con los campos "rules" y "weeks".'
  prompt += 'Te voy a enviar una consulta de un usuario que contiene un conjunto de reglas para llevar a cabo durante un cierto numero de semanas de la simulacion.'
  prompt = 'Esta es la informacion proporcionada por el usuario:\n'
  prompt += f'"{rules}."\n'
  prompt += 'En dependencia a la informacion ingresada, procesa los datos y devuelveme un objeto tipo json con la siguiente estructura:\n'
  prompt += '"rules": "resumen de las reglas del usuario",\n'
  prompt += '"weeks": "un entero que represente solamente la cantidad de semanas durante las cuals el usuario quiere llevar a cabo las reglas"\n'
  prompt += 'Necesito que la informacion almacenada en el objeto .json sea lo mas concreta y objetiva posible'
  return prompt