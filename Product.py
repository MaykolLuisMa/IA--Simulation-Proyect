from typing import List
class Product:
    def __init__(self,id : int,name : str,type):
        self.id = id
        self.name = name
        self.type = type

class Product_in_sale:
    def __init__(self, product : Product, price : float, amount : int):
        self.product = product
        self.price = price
        self.amount = amount

class Product_to_buy:
    def __init__(self, product : Product, amount : int):
        self.product = product
        self.amount = amount




