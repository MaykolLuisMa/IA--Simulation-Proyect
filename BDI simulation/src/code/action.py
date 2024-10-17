#dependencias
from src.code.product import *
from src.utils import pen

#estado de los "ProductMount"
class State:
  def __init__(self, product_mount: list[ProductMount], scores: dict[Product, float]):
    self._product_mount = product_mount
    self._scores = self._set_scores(scores) if len(scores) != 0 else 0
    
  #puntuacion de un "State"
  def _set_scores(self, scores: dict[Product, float]) -> float:
    result = 0
    total = 0
    
    for products in self._product_mount:
      result += scores[products.product] * products.mount
      total += products.mount
      
    return result /total
  
  @property  
  def product_mount(self) -> list[ProductMount]:
    return self._product_mount

  @property
  def score(self) -> float:
    return self._scores
  
#Nodo para manejar la funcion de costo de un estado
class Node:
  def __init__(self, state: State, cost: float):
    self._product_mount = state.product_mount
    self._score = state.score - cost
    
  @property
  def product_mount(self) -> list[ProductMount]:
    return self._product_mount
  
  @property
  def score(self) -> float:
    return self._score
  
#agente BDI
class AgentBDI:
  def __init__(self, transactions: list[ProductMount], last_products: list[ProductMount], market_products: list[ProductMount],
               beliefs: list, products: list[ProductMount], week: int):
    self._beliefs = beliefs
    self._week = week
    self._current_products = products
    self._products_score = self._score_products(transactions, products) #puntuacion de cada producto en dependencia de lo que vendi respecto a lo que tenia
    self._products_limit = self._limits(products) #limite de cada producto
    self._last_products = last_products
    self._market_products = market_products
    
  #puntuar los productos 
  def _score_products(self, transactions: list[ProductMount], products: list[ProductMount]) -> dict[Product, float]:
    result = {}
    
    for product_mount in products:
      aux = product_mount.product
      result[aux] = 0
      
      for transaction in transactions:
        if transaction.product.name == aux.name:
          result[aux] = transaction.mount / product_mount.mount 
          break
    
    return result
  
  #fijar el limite de cada producto para la generacion de "states" 
  def _limits(self, products: list[ProductMount]) -> dict[Product, int]:
    result = {}

    for product in products:
      aux = product.product
      result[aux] = product.mount + int(product.mount * self._products_score[aux])
      
    return result
  
  #generar estados A*
  def _gen_states_ia(self, products: list[ProductMount], market: list[ProductMount]) -> list[State]:
    result = []
    self._gen_states_rec_ia(products, 0, [], result)
    
    if len(result) == 0:
      products = []
      
      for product_mount in market:
        products.append(ProductMount(product_mount.product, int(product_mount.mount * pen(max=0.15))))
      
      result.append(State(products, self._products_score))
      
    return result
    
  def _gen_states_rec_ia(self, products: list[ProductMount], iter: int, temp: list[ProductMount], result: list[State]):
    if iter == len(products):
      if len(temp) != 0:
        result.append(State(temp, self._products_score))
    
    else:
      i = 0
      aux = products[iter].product

      while True:  
        if i * 10 > self._products_limit[aux]:
          break
        
        self._gen_states_rec_ia(products, iter + 1, temp + [ProductMount(products[iter].product, i * int(self._products_limit[aux] / 10) if self._products_limit[aux] > 10 else 1)] if i != 0 else temp, result)
        i += 1
  
  #returna el believe que mejor matchea
  def _best_belief(self) -> str | None:
    for belief in self._beliefs:
      if belief[1] == self._week:
        return belief[0]
    
    return None
  
  #acciones del agente BDI
  def action(self) -> list[State]:
    belief = self._best_belief()
    
    if belief == None:
      return self._gen_states_ia(self._last_products, self._market_products)
    
    return self._gen_states_bdi(belief)
  
  def _gen_states_bdi(self, belief: str) -> list[State]:
    #clonamos los productos y el producto a generar lo ponemos al final
    temp = [x for x in self._current_products if x.product.name != belief] + [None]
    result = []
    
    for products in self._current_products:
      if products.product.name == belief:
        limit = self._products_limit[products.product]
        contador = 1
        plot = int(self._products_limit[products.product] / 10) if self._products_limit[products.product] > 10 else 1 
        
        while True:
          gen = contador * plot
          temp[-1] = (ProductMount(products.product, products.mount + gen))
          result.append(State([x for x in temp], self._products_score))
          contador += 1
          
          if gen > limit:
            break
    
    return result
  