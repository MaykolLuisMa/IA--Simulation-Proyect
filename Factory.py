from typing import List,Dict,Tuple
from Product import AccountedProduct, ProductCollection

class Factory:
    def __init__(self,id,name,building_cost : float,
                 basic_operation_cost : float,
                 time_to_build : int,
                 product_limit : int,
                 necessary_products : ProductCollection,
                 produced_products : ProductCollection):
        self.id = id
        self.name = name
        self.building_cost = building_cost
        self.basic_operation_cost = basic_operation_cost
        self.time_to_build = time_to_build
        self.product_limit = product_limit
        self.necessary_products = necessary_products
        self.produced_products = produced_products
    
    def get_max_necessary(self):
        return ProductCollection([AccountedProduct(p.product, p.amount*self.product_limit) for p in self.necessary_products])
    
    def get_operation_cost(self,personal):
        return (self.basic_operation_cost*4/10)+((self.basic_operation_cost*6/10)*(personal.basic_price/10))

    def get_building_cost(self,inflation_factor):
        return self.building_cost*inflation_factor
    def __eq__(self, other : object) -> bool:
        return self.id == other.id
    def __hash__(self) -> int:
        return self.id.__hash__()    
    def calculate_alpha(self,products : ProductCollection, alpha = 1):
        used = {p.product.id: p.amount*alpha for p in self.necessary_products}
        if (alpha <= self.product_limit) and all((used[p.product.id] <= p.amount) for p in products):
            return self.calculate_alpha(products,alpha+1)
        else:
            return alpha-1
    
    def produce(self,products : ProductCollection):
        products = sorted(products, key=lambda p : p.product.id)
        alpha = self.calculate_alpha(products)
        necesary = ProductCollection([AccountedProduct(p.product,-p.amount*alpha) for p in self.necessary_products])
        produced = ProductCollection([AccountedProduct(p.product,p.amount*alpha) for p in self.produced_products])
        return necesary, produced
    
def produce_for_all_factories(products : ProductCollection, factories : Tuple[Factory,int]):
    factory = Factory(factories[0].id,factories[0].name,factories[0].building_cost, factories[0].basic_operation_cost, factories[0].time_to_build,factories[1]*factories[0].product_limit, factories[0].necessary_products, factories[0].produced_products)
    return factory.produce(products)

def calculate_build_cost(factory : Factory, factories : Dict[Factory,int],inflation_factor):
    factories_list = list(factories.keys())
    if factories_list == 1 and factories_list[0].id == factory.id:
        return factory.get_building_cost(inflation_factor)*70/100
    if any(f.id == factory.id for f in factories):
        return factory.get_building_cost(inflation_factor)*90/100
    return factory.get_building_cost(inflation_factor)

def calculate_operation_cost(factory : Factory,personal, factories : Dict[Factory,int]):
    factories_list = list(factories.keys())
    if factories_list == 1 and factories_list[0].id == factory.id:
        return factory.get_operation_cost(personal)
    else:
        return factory.get_operation_cost(personal)*110/100
        