from simulation.Product import Product, Product_in_sale, AccountedProduct,ProductCollection
from simulation.Company import Company,Seller,Buyer, Global_Company,get_company_value, build_factory, get_company_storage_limit
from simulation.Market import Market
from typing import List
from simulation.Condition import Adaptation_5_porcent, Hyerinflation
from simulation.State import State
from simulation.Factory import Factory
import utils
import random
from Algorithms import uniform_cost_search_algorithm, random_algorithm, coin_greedy_algorithm, pib_greedy_algorithm

product_list = [Product(0,"porc","food",2000),Product(1,"swine meat","food",15)]#,Product(1,"chicken","food"),Product(1,"pork","food"),Product(1,"shrims","food")]

factory_list = [Factory(1,"Abattoir(pork)",5000,200,1,15,
                    ProductCollection([AccountedProduct(product_list[0],1)])
                    ,[AccountedProduct(product_list[1],150)])
                    ]
company_list = [Company(0,"White Spider",100000,ProductCollection([AccountedProduct(product_list[0],10),AccountedProduct(product_list[1],1000)]),{factory_list[0]:1},100,random_algorithm)]

def products_generator(products : List[Product]):
    amounts = [random.randrange(0,1000) for p in products]
    in_sale = [Product_in_sale(p,p.basic_price,amounts[i]) for i,p in enumerate(products)]
    to_buy = [AccountedProduct(p,amounts[i]) for i,p in enumerate(products)]
    return in_sale,to_buy
in_sale,to_buy = products_generator(product_list)
in_sale = ProductCollection(in_sale)
to_buy = ProductCollection(to_buy)
global_seller = Seller(Global_Company(),in_sale)
global_buyer = Buyer(Global_Company(),to_buy)


market = Market(global_seller,global_buyer,product_list)
initial_state = State(company_list,market,factory_list,[],[],[Adaptation_5_porcent()])

inflationfactor = market.get_inflation_factor()


#print([[p.product.name, p.amount] for p in get_company_storage_limit(company_list[0])])
#build_factory(company_list[0],initial_state,factory_list[0])
#print([[p.product.name, p.amount] for p in get_company_storage_limit(company_list[0])])
#build_factory(company_list[0],initial_state,factory_list[0])
#print([[p.product.name, p.amount] for p in get_company_storage_limit(company_list[0])])
#print(f"Inflation {inflationfactor}")
#print(F"Factories {company_list[0].factories}")
#print(f"Company operation cost: {company_list[0].get_operation_cost(inflationfactor)}")
#print(f"Company value {get_company_value(company_list[0],market)}")

