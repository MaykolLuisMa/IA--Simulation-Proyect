import random
import math
import heapq
from typing import List
def normal_variation(value : float, variation = 0.03):
    return value
    return np.random.normal(value, value*variation, None)

def uniform_variation(low, high):
    return random.uniform(low,high)

def random_up(value : int, porcent = 0.05):
    high = int(value * (1 + porcent))
    if value == high:
        return value
    return random.uniform(value,high)

def random_down(value : int, porcent = 0.05):
    low = int(value * (1 - porcent))
    low = max(0,low)
    return random.uniform(low,value)

def adjust_value(current_value, posible_new_value,variaton_limit = 0.15):
    up = (1+variaton_limit)*current_value
    down = (1-variaton_limit)*current_value

    if current_value == posible_new_value:
        return current_value
    elif current_value < posible_new_value:
        if posible_new_value <= up:
            return posible_new_value
        else:
            return random_up(current_value,variaton_limit)
    elif current_value > posible_new_value:
        if posible_new_value >= down:
            return posible_new_value
        else:
            return random_down(current_value,variaton_limit)
def get_porcent(total,part):
    return part/total

def normalize_price(price, price_reference, current_price):
    porcent = get_porcent(price_reference,current_price)
    return price/porcent


class PriorityQueue:
    def __init__(self, items=(), key=lambda x: x): 
        self.key = key
        self.items = []
        for item in items:
            self.add(item)
         
    def add(self, item):
        """Add item to the queuez."""
        pair = (self.key(item), item)
        heapq.heappush(self.items, pair)

    def pop(self):
        """Pop and return the item with min f(item) value."""
        return heapq.heappop(self.items)[1]
    
    def top(self): return self.items[0][1]

    def __len__(self): return len(self.items)

def add_products(products1 : List, products2 : List):
        products = []
        index = 0
        if type(products1[0]) == float and type(products2[0]) == float:
            products.append(products1[0]+products2[0])
            index = 1
        temporal = []
        temporal.extend(products1[index:])
        temporal.extend(products2[index:])
        temporal_set = set(temporal)

#devolver si una cadena es un numero y en caso de serlo, devolver el numero
def is_int(num: str):
  try:
    parse = int(num)
    return (True, parse)
  
  except:
    return (False, None)

#de una lista de elementos y una cadena, tomar la interseccion
def clean_query(products: list, query: str) -> list:
  result = []
  parse = query.split(' ')
  
  for element in parse:
    if element in products:
      result.append({'value': element, 'type': 'product'})
    
    elif element == 'o' or element == 'y':
      if result[-1] != 'o' and result[-1] != 'and':
        result.append({'value': element, 'type': 'operator'})
  
  return result 

#mostrar una cadena a partir de una lista, para brindar legibilidad al LM
def show_list(list: list):
  result = ''
  
  for i in range(len(list)):
    result += f'{list[i]}, ' if i < len(list) - 1 else list[i]
    
  return result

#crear una copia de los elementos de una lista
def clone(list: list):
  result = []
  
  for element in list:
    result.append(element) 
  
  return result