from typing import Any, List, Tuple
class Product:
    def __init__(self,id : int,name : str,type, basic_price):
        self.id = id
        self.name = name
        self.basic_price = basic_price
        self.type = type
    def __eq__(self, other: object) -> bool:
        if other == None:
            return False
        return self.id == other.id

class AccountedProduct:
    def __init__(self, product : Product, amount : int):
        self.product = product
        self.amount = amount
    
    def __add__(self, other):
        return AccountedProduct(self.product, self.amount + other.amount)
    
    def __eq__(self, other: object) -> bool:
        return self.product == other.product 
    
    def __sub__(self, other):
        return AccountedProduct(self.product,self.amount-other.amount)
         
class Product_in_sale(AccountedProduct):
    def __init__(self, product : Product, price : float, amount : int):
        super().__init__(product,amount)
        self.price = price
        
    def get_total_price(self):
        return self.amount*self.price

    def __add__(self, other):
        return Product_in_sale(self.product, self.price, self.amount + other.amount)
    
    def __sub__(self, other):
        return Product_in_sale(self.product,self.price,self.amount-other.amount)

class market_Product_Dates:
    def __init__(self, product : Product, price : float, offert : Tuple[int,int], demand : Tuple[int,int]):
        self.product = product
        self.price = price
        self.external_market_offert = offert[0]
        self.general_offert = offert[1]
        self.external_market_demand = demand[0]
        self.general_demand = demand[1]


class ProductCollection:
    def __init__(self, col : List,coin = 0) -> None:
        self.col = {}
        self.coin = coin
        for p in col:
            if type(p) == Product:
                self.col[p.id]=p
            elif type(p) == AccountedProduct or type(p) == Product_in_sale:
                self.col[p.product.id]=p

    def append(self,product : Product, amount : int):
        if product == None:
            self.coin += amount
            return
        elif product.id in self.col:
            self.col[product.id].amount += amount
        else:
            self.col[product.id] = AccountedProduct(product,amount)
    
    def __iter__(self):
        return iter(self.col.values())
    
    def extract(self, product : Product,amount):
        if product == None:
            self.coin += amount
            return
        self.col[product.id].amount -= amount
    
    def is_positive(self):
        if self.coin < 0:
            return False
        return all([p.amount >= 0 for p in self])
    
    def get(self, product_id):
        return self.col[product_id]
    
    def opponent(self):
        opp = ProductCollection([])
        for p in self.col:
            if type(p) == int or type(p) == float:
                opp.coin = -p
            elif type(p) == AccountedProduct:
                opp.append(AccountedProduct(p.product,-p.amount))
            elif type(p) == Product_in_sale:
                opp.append(Product_in_sale(p.product,p.price,-p.amount))
        return opp
    def __len__(self):
        return len(self.col.items())
class Personal(Product):
    def __init__(self):
        super().__init__(-1, "Personal", "personal", 10)

def add_products(products1 : ProductCollection, products2 : ProductCollection):
        products = ProductCollection([])
        for p in products1:
            products.append(p.product,p.amount)
        for p in products2:
            products.append(p.product,p.amount)
        products.coin = products1.coin + products2.coin
        return products
        

        