#dependencias
import json

#respuesta parseada
def parse_json(json_data: str) -> dict:
  result = json.loads(json_data) #parsear de json a dict
  return result