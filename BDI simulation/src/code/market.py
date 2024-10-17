#dependencias
from src.code.company import Factory
from src.code.product import ProductMount, Product
from src.code.sale import tec_factory, tec_products
from src.utils import pen

#venta
class Sale: 
  def __init__(self, clasification: str, factory: Factory, products: list[ProductMount]) -> None:
    self._clasification = clasification
    self._factory = factory
    self._products = products
    
  @property
  def clasification(self) -> str:
    return self._clasification
  
  @property
  def factories(self) -> list[Factory]:
    return self._factories
  
  @property
  def products(self) -> list[ProductMount]:
    return self._products

#mercado
class Market:  
  def __init__(self):
    self._tec = self._gen(tec_products, tec_factory, 'tecnology')
    #self._transport = self._gen(transport_raw, transport_factory, 'transport')
    self._products = [self._tec]
    
  #generar los "ProductMount" con una penalizacion aleatoria  
  def _gen(self, list_products: list[ProductMount], factory: Factory, clasification: str) -> Sale:
    products_market = list(map(lambda x: ProductMount(x.product, int(x.mount * pen(min=0.7))), list_products))
    return Sale(clasification, factory, products_market)
  
  @property
  def products(self) -> list[Sale]:
    return self._products
  