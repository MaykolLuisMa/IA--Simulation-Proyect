from typing import List, Tuple
class Product:
    def __init__(self,id : int,name : str,type, basic_price):
        self.id = id
        self.name = name
        self.basic_price = basic_price
        self.type = type

class Product_in_sale:
    def __init__(self, product : Product, price : float, amount : int):
        self.product = product
        self.price = price
        self.amount = amount
    def get_total_price(self):
        return self.amount*self.price
class Product_to_buy:
    def __init__(self, product : Product, amount : int):
        self.product = product
        self.amount = amount

class Marquet_Product_Dates:
    def __init__(self, product : Product, price : float, offert : Tuple[int,int], demand : Tuple[int,int]):
        self.product = product
        self.price = price
        self.external_marquet_offert = offert[0]
        self.general_offert = offert[1]
        self.external_marquet_demand = demand[0]
        self.general_demand = demand[1]


def get_product_list() -> List[Product]:
    return [Product(1,"rice","food",10)]#,Product(1,"chicken","food"),Product(1,"pork","food"),Product(1,"shrims","food")]

class Personal(Product):
    def __init__(self):
        super().__init__(0, "Personal", "personal", 10)