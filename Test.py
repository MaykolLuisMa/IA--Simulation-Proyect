from simulation.Product import Product, Product_in_sale, AccountedProduct
from simulation.Company import Company,Seller,Buyer, Global_Company
from simulation.Market import Market
from typing import List
from main import Simulation
from simulation.Condition import Adaptation_5_porcent
import random
from Algorithms import a_star_algorithm
def get_product_list() -> List[Product]:
    return [Product(1,"rice","food",10)]#,Product(1,"chicken","food"),Product(1,"pork","food"),Product(1,"shrims","food")]

def products_in_sale_generator(products : List[Product]):
    return [Product_in_sale(p,random.randrange(1,20),random.randrange(0,1000)) for p in products]

def products_to_buy_generator(products : List[Product]):
    return [AccountedProduct(p,random.randrange(0,1000)) for p in products]

products = get_product_list()
global_seller = Seller(Global_Company(),products_in_sale_generator(products))
global_buyer = Buyer(Global_Company(),products_to_buy_generator(products))
company = Company(0,"White Spider",10000,products_to_buy_generator(products),[],10,a_star_algorithm)
Market = Market(global_seller,global_buyer)
sim = Simulation([],Market,[],[],[],[Adaptation_5_porcent()])
sim.ejecution()

