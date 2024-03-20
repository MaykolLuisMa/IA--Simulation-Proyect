from typing import List
from Product import Product_to_buy
class Factory:
    def __init__(self,id,name,cost : float,
                 time_to_build : int,
                 production_limit : List[int],
                 necessary_products : List[Product_to_buy],
                 produced_products : List[Product_to_buy]):
        self.id = id
        self.name = name
        self.cost = cost
        self.time_to_build = time_to_build
        self.production_limit = production_limit
        self.necessary_products = necessary_products
        self.produced_products = produced_products
    def __eq__(self, other : object) -> bool:
        return self.id == other.id
            
            
   
