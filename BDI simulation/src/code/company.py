#dependencias
from src.code.action import AgentBDI, State, Node
from src.code.product import *
from src.utils import pen, clone

#factoria
class Factory:
  def __init__(self, clasification: str, price=100000.0):
    self._clasification = clasification #tipo de productos que produce
    self._price = price #precio de la factoria
    self._active = True #saber si la factoria esta o no en condiciones de usarse
    self._reparation = 0 if self._active else price * pen(max=0.25) #precio de arreglar la factoria
    
  #producir en una cierta cantidad  
  def produce(self, product: Product, cant: int) -> ProductMount:
    return ProductMount(Product(product.name, self._clasification, product.price * 1.5, product.requirements), cant)
   
  #arreglar la factoria
  def activate(self):
    self._active = True
   
  @property
  def clasification(self) -> str:
    return self._clasification

  @property
  def price(self) -> int:
    return self._price 

  @property
  def active(self) -> bool:
    activation = True if pen() >= 0.15 else False
    self._active = activation
    return self._active

  @property
  def reparation(self) -> float:
    return self._reparation
 
#empresa
class Company:
  def __init__(self, name: str, presp=1000000.0):
    self._name = name #nombre de la empresa
    self._presp = presp #presupuesto de la empresa
    self._factories = [] #factorias que posee
    self._products = [] #productos
    self._last_products = [] #productos de la semana anterior
    self._transactions = {} #ventas por semana
    self._beliefs = [] #creencias de la empresa
  
  #actualizar los beliefs
  def add_belief(self, rule: str, week: int):
    if 'celular' in rule.lower():
      self._beliefs.append(('celular', week))
      
    if 'computadora' in rule.lower():
      self._beliefs.append(('computadora', week))
    
  #factoria que produce un producto
  def _get_factory(self, product: Product) -> Factory:
    for factory in self._factories:
      if factory.clasification == product.clasification:
        return factory
  
  #agregar una cantidad de un producto
  def _add_product(self, product_mount: ProductMount):
    for i in range(len(self._products)):
      if self._products[i].product.name == product_mount.product.name:
        self._products[i] = ProductMount(self._products[i].product, self._products[i].mount + product_mount.mount)
        return
    
    self._products.append(product_mount)
   
  #eliminar un producto vendido 
  def _delete_product(self, product: ProductMount):
    for i in range(len(self._products)):
      if self._products[i].product.name == product.product.name:
        self._products[i] = ProductMount(self._products[i].product, self._products[i].mount - product.mount)
        
        if self._products[i].mount == 0:
          del self._products[i]
        break

          
  #producir un producto en cierta cantidad
  def _produce(self, product: Product, cant: int) -> bool:
    factory = self._get_factory(product)  
    
    if not factory.active:
      self._fix_factory(factory)
       
    production = factory.produce(product, cant)
    self._add_product(production)
    
    for product_mount in product.requirements:
      self._delete_product(product_mount)
  
  #construir una factoria
  def _build(self, factories: list[Factory], product: Product) -> Factory:
    for factory in factories:
      if factory.clasification == product.clasification:
        temp = Factory(factory.clasification, factory.price)
        self._factories.append(temp)
        self._presp -= factory.price
        return temp
  
  #comprar productos
  def _buy(self, materials: list[ProductMount]):
    for product_mount in materials:
      self._presp -= product_mount.mount * product_mount.product.price
      self._add_product(product_mount)
  
  #arreglar una factoria
  def _fix_factory(self, factory: Factory):
    factory.activate()
    self._presp -= factory.reparation
  
  #vender productos
  def sell(self, products: ProductMount):
    self._presp += products.mount * products.product.price
    self._delete_product(products)
  
  #accion de cada empresa 
  def action(self, materials: list[ProductMount], factory: Factory, transactions: list[ProductMount], 
             week: int) -> str:
    agent = AgentBDI(transactions, self._last_products, materials, self._beliefs, self._products, week)
    states = agent.action()
    nodes = []
    
    for state in states:
      if self._valid(state.product_mount):
        nodes.append(self._action(state, materials, [factory], True))
      
    nodes.sort(key=lambda x: x.score)
    nodes.reverse()
    
    for node in nodes:
      result = self._action(node, materials, [factory], False)
      self._last_products = clone(self._products)
      return result
    
    return f'La empresa {self._name} quebro.\n'
  
  def _action(self, production: State | Node, material_market: list[ProductMount], factories_market: list[Factory], 
              clon: bool) -> str | Node:
    temp = self._clone_company() if clon else self #si le pasamos 'clon=true' significa que creamos una simulacion interna
    inform = '' #iniciamos el informe
    
    for products in production.product_mount:
      #inicialmente la diferencia entre un producto 'A' mio y uno 'A' que debo generar es 'None'
      rest = None
      
      for product_mount in temp.products:
        if product_mount.product.name == products.product.name:
          rest = products.mount - product_mount.mount
          break
      
      #si no tengo el producto la diferencia es el producto a generar
      if rest == None:
        rest = products.mount
      
      #compramos los requerimientos del producto 
      for req in products.product.requirements:
        for materials in material_market:
          if materials.product.name == req.product.name:
            temp._buy([ProductMount(materials.product, req.mount * rest)])
            inform += f'La empresa "{temp._name}" compro {req.mount * 10} unidades del producto "{materials.product.name}" a {materials.product.price} dolares cada unidad quedandose con un presupuesto de {temp._presp} dolares.\n'
            break
      
      #si no tenemos una factoria para producir un producto, construimos una    
      if temp._get_factory(products.product) == None:
        factory = temp._build(factories_market, products.product)
        inform += f'La empresa {temp.name} construyo una factoria por el precio de {factory.price} dolares de tipo "{factory.clasification}", quedandose con un presupuesto de {temp._presp} dolares.\n'

      temp._produce(products.product, rest)
      inform += f'La empresa {temp.name} produjo {rest} unidades del producto "{products.product.name}" quedandose con un presupuesto de {temp._presp} dolares.\n'
    
    cost = (self._presp - temp._presp)
    
    if clon: 
      return Node(production, cost / self._presp)
    
    return inform
    
  #clonar una empresa
  def _clone_company(self) -> 'Company':
    clon = Company('clon', self._presp)
    clon._factories = clone(self._factories)
    clon._products = clone(self._products)
    return clon
  
  #saber si un estado es valido
  def _valid(self, state: list[ProductMount]) -> bool:
    for products in state:
      for product_mount in self._products:
        if products.product == product_mount.product and products.mount < product_mount.mount:
          return False
          
    return True
     
  @property
  def name(self) -> str:
    return self._name
  
  @property
  def clasification(self) -> str:
    return self._clasification
  
  @property
  def products(self) -> list[ProductMount]:
    return self._products
  