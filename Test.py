from Product import Product, Product_in_sale, Product_to_buy
from Company import Company,Seller,Buyer, Global_Company
from Marquet import Marquet
from typing import List
from program import Simulation
from Condition import Adaptation_5_porcent
import random

def get_product_list() -> List[Product]:
    return [Product(1,"rice","food",10)]#,Product(1,"chicken","food"),Product(1,"pork","food"),Product(1,"shrims","food")]

def products_in_sale_generator(products : List[Product]):
    return [Product_in_sale(p,random.randrange(1,20),random.randrange(0,1000)) for p in products]

def products_to_buy_generator(products : List[Product]):
    return [Product_to_buy(p,random.randrange(0,1000)) for p in products]

products = get_product_list()
global_seller = Seller(Global_Company(),products_in_sale_generator(products))
global_buyer = Buyer(Global_Company(),products_to_buy_generator(products))
company = Company(0,"White Spider",10000,products_to_buy_generator(products),[],10)
marquet = Marquet(global_seller,global_buyer)
sim = Simulation([],marquet,[],[],[],[Adaptation_5_porcent()])
sim.ejecution()
