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
def rules_prompt(rules: str, products: str, keywords: str, actions: str):
  prompt = 'A continuacion te voy a enviar un conjunto de palabras clave:\n'
  prompt += f'"{keywords}".\n'
  prompt += 'Ahora te voy a enviar una consulta de un usuario que va a referirse a algunos de los siguientes productos y va a realizar una accion especifica:\n'
  prompt += f'"{products}".\n'
  prompt += 'Esta es la consulta:\n'
  prompt += f'{rules}.\n'
  prompt += 'Necesito que me envies un objeto tipo json con la siguiente estructura:\n'
  prompt += 'Cada llave es cada producto que aparezca en la consulta del usuario y su respectivo valor es una de las palabras claves que te proporcione, depende a la que mas se asemeje a la descripcion del producto proporcionada por el usuario en la consulta.'
  prompt += 'Ahora te voy a enviar un conjunto de acciones:\n'
  prompt += f'"{actions}".\n'
  prompt += f'Ademas agrega un campo llamado "action", donde solamente quiero que me almacenes objeto tipo list de 2 posiciones donde el primer elemento sea la accion correspndiente y el segundo elemento una de las palabras claves siguientes: "{keywords}".\n'
  prompt += 'Necesito la respuesta lo mas objetiva posible no quiero en el json campos que no sean productos y en el campo "action" una lista de 2 elementos'
  return prompt