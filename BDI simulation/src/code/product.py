#producto
class Product:
  def __init__(self, name: str, clasification: str, price: float, requirements: list['ProductMount']):
    self._name = name #nombre del producto
    self._clasification = clasification #clasificacion del producto
    self._price = price #precio por unidad
    self._requirements = requirements #requerimientos de un producto
    
  @property
  def name(self) -> str:
    return self._name
  
  @property
  def clasification(self) -> str:
    return self._clasification
  
  @property
  def requirements(self) -> list['ProductMount']:
    return self._requirements
  
  @property
  def price(self):
    return self._price
  
#cantidad de productos por unidad
class ProductMount:
  def __init__(self, product: Product, mount: int):
    self._product = product #producto que maneja
    self._mount = mount #cantidad de unidades del producto
    
  @property
  def product(self) -> Product:
    return self._product
   
  @property
  def mount(self) -> int:
    return self._mount
  