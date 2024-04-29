import fuzzy as fz
import numpy as np

from search.Graph_Search_Algorhitms import uniform_cost_search, get_next_node, greedy, random_search
from search.Node import Node
from search.Actions_result import Action
from simulation.Company import Company, can_produce, can_used, sell, build_factory, buy, produce
from simulation.State import State
from simulation.Product import Product



def get_company_action(company : Company, state):
    return company.algorthm(company, state)
 
def uniform_cost_search_algorithm(company, state):

    node = Node(company,state,None,None,0,0)
    goal_node = uniform_cost_search(node)
    next_node = get_next_node(node,goal_node)
    return next_node.action


def only_fuzzy_algorithm(company: Company, state: State):
    
    priority_universe = np.arange(0, 10, 1)
    priority_membresy_sell = {}
    priority_membresy_buy = {}
    ## --- produced products --- ##
    produced_products: list[Product] = [x for x in company.products if not can_used(company, x)]
    produced_products_universe = fz.product_universes(company, produced_products)
    produced_products_ant = fz.product_membresy_functions(produced_products_universe, produced_products, True)
    
    ## --- raw material --- ##
    raw_material: list[Product] = [x for x in company.products if not can_produce(company, x)]
    raw_material_universe = fz.product_universes(company, raw_material)
    raw_material_ant = fz.product_membresy_functions(raw_material_universe, raw_material, True)


    produced_products_con = fz.product_membresy_functions(produced_products_universe, produced_products, False)
    sell_product_rules = []
    buy_product_rules = []
    produce_rules = []
    
    for product in produced_products:
        priority = fz.ctrl.Consequent(priority_universe, f'sell {product.id}')
        priority_membresy_sell[f'sell {product.id}'] = priority
        priority.automf(5)
        sell_product_rules.append(fz.ctrl.rule(produced_products_ant[product.id]['poor'] ,priority['poor']))
        sell_product_rules.append(fz.ctrl.rule(produced_products_ant[product.id]['mediocre'] ,priority['mediocre']))
        sell_product_rules.append(fz.ctrl.rule(produced_products_ant[product.id]['average'] ,priority['average']))
        sell_product_rules.append(fz.ctrl.rule(produced_products_ant[product.id]['decent'] ,priority['decent']))
        sell_product_rules.append(fz.ctrl.rule(produced_products_ant[product.id]['good'] ,priority['good']))


    for product in raw_material:
        priority = fz.ctrl.Consequent(priority_universe, f'buy {product.id}')
        priority_membresy_buy[f'buy {product.id}'] = Action(sell, state, [product])
        priority.automf(5)
        buy_product_rules.append(fz.ctrl.rule(raw_material_ant[product.id]['poor'] ,priority['poor']))
        buy_product_rules.append(fz.ctrl.rule(raw_material_ant[product.id]['mediocre'] ,priority['mediocre']))
        buy_product_rules.append(fz.ctrl.rule(raw_material_ant[product.id]['average'] ,priority['average']))
        buy_product_rules.append(fz.ctrl.rule(raw_material_ant[product.id]['decent'] ,priority['decent']))
        buy_product_rules.append(fz.ctrl.rule(raw_material_ant[product.id]['good'] ,priority['good']))
    
    




def greedy_algorithm(company, state):
    node = Node(company,state,None,None,0,0)
    next_node = greedy(node)
    return next_node.action

def random_algorithm(company, state):
    node = Node(company,state,None,None,0,0)
    next_node = random_search(node)
    return next_node.action                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
