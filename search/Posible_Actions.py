from simulation.Company import Company, produce, buy, sell, build_factory, get_company_storage_limit
from simulation.State import State
from simulation.Product import AccountedProduct,ProductCollection,Product_in_sale, add_products
from simulation.Factory import Factory, calculate_build_cost
from typing import List
from copy import deepcopy
class Action:
    def __init__(self, f, company, state,args : List) -> None:
        self.f = f
        self.company = company
        self.state = state
        self.args = args 
    def ejecute_action(self):
        self.f(self.company,self.state,*self.args)

    def __str__(self) -> str:
        if self.f == None:
            return "Nothing"
        return self.f.__name__

def action_cost(company,past_state : State,new_state : State,action : Action):
    return 1


def determinate_posible_actions(company : Company, state : State):
    actions = []
    actions += posible_factory_build(company,state)
    actions += posible_buys(company,state)
    actions += posible_sells(company, state)
    actions += posible_produces(company,state)
    return [deepcopy(act) for act in actions]

def posible_factory_build(company : Company, state : State):
    actions = []
    for f in state.factories:
        build_cost = calculate_build_cost(f,company.factories,state.market.get_inflation_factor())
        operation_cost = company.get_operation_cost(state.market.get_inflation_factor())
        if(company.coin >= build_cost + operation_cost):
            actions.append(Action(build_factory,company,state,[f]))
    return actions
def posible_sells(company : Company, state : State):
    actions = []
    for p in company.products:
        product_in_sale = Product_in_sale(p.product,state.market.get_global_seller().in_sale.get(p.product.id).price,p.amount)
        actions.append(Action(sell,company, state, [ProductCollection([product_in_sale])]))
    return actions

def posible_buys(company : Company, state):
    actions = []
    products = company.products.opponent()
    products = add_products(products, get_company_storage_limit(company))
    for p in products:
        actions.append(Action(buy,company,state,[ProductCollection([p])]))
    return actions

def posible_produces(company : Company, state : State):
    actions = []
    for f_i in company.factories.items():
        actions.extend(posible_produces_by_factory(company,state,company.products,f_i))
    return actions

def posible_produces_by_factory(company : Company,state,disponible_products : ProductCollection,
                     factory):
    alpha = factory[0].calculate_alpha(disponible_products)*factory[1]
    if alpha == 0:
        return []
    actions = []
    for i in range(1,alpha):
        necesary_products = ProductCollection([AccountedProduct(p.product,p.amount*i) for p in factory[0].necessary_products])
        actions.append(Action(produce, company,state,[necesary_products,(factory[0],i)]))
    return actions