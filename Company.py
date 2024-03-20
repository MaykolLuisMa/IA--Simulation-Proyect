from typing import List, Dict
from Product import Product_to_buy, Product_in_sale
from Factory import Factory
from Marquet import Marquet
class Company:
    def __init__(self, id : int, name : str, coin : float, products : List[Product_to_buy], factories : Dict[Factory : int]):
        self.id = id
        self.name = name
        self.coin = coin
        self.products = products
        self.factories = factories
    def sell(self, marquet : Marquet, products : List[Product_to_buy]):
        pass
    def buy(self, marquet : Marquet, products : List[Product_to_buy]):
        pass
    
    def build_factory(self, factory : Factory):
        if self.coin < factory.cost:
            return
        self.coin -= factory.cost
        if factory in self.factories:
            self.factories[factory] += 1
        else:
            self.factories[factory] = 1
            
    def process(self, products : List[Product_to_buy], factory : Factory):
        pass


class Seller:
    def __init__(self, company : Company, in_sale : List[Product_in_sale]):
        self.company = company
        in_sale = in_sale

class Buyer:
    def __init__(self, company : Company, to_buy : List[Product_to_buy]):
        self.company = company
        self.to_buy = to_buy