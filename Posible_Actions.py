from Company import Company, produce, buy, sell, build_factory
from State import State
from Product import AccountedProduct,ProductCollection,Product_in_sale, add_products
from Factory import Factory
from typing import List
class Action:
    def __init__(self, f, company, state,args : List) -> None:
        self.f = f
        self.company = company
        self.state = state
        self.args = args 
    def ejecute_action(self):
        self.f(self.company,self.state,*self.args)

def action_cost(company,past_state : State,new_state : State,action : Action):
    return 1


def determinate_posible_actions(company : Company, state : State):
    actions = []
    actions += posible_factory_build(company,state)
    actions += posible_buys(company,state)
    actions += posible_sells(company, state)
    actions += posible_produces(company,state)
    return actions

def posible_factory_build(company : Company, state : State):
    actions = []
    for f in state.factories:
        build_cost = f.get_building_cost(state.market.get_inflation_factor())
        if(company.coin >= build_cost):
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
    for f in company.factories:
        products = add_products(products,f.get_max_necessary())
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
    for i in range(alpha):
        necesary_products = ProductCollection([AccountedProduct(p.product,p.amount*i) for p in factory[0].necessary_products])
        actions.append(Action(produce, company,state,[necesary_products,(factory[0],i)]))
    return actions