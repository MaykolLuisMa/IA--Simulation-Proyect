from Graph_Search_Algorhitms import uniform_cost_search, get_next_node, greedy, random_search
from Node import Node
from Company import Company, can_produce, can_used
import fuzzy as fz
from State import State
import numpy as np

def get_company_action(company : Company, state):
    return company.algorthm(company, state)
 
def uniform_cost_search_algorithm(company, state):

    node = Node(company,state,None,None,0,0)
    goal_node = uniform_cost_search(node)
    next_node = get_next_node(node,goal_node)
    return next_node.action


def only_fuzzy_algorithm(company: Company, state: State):
    priority_universe = np.arange(0, 10, 1)
    priority_membresy_sell = []
    produced_products = [x for x in company.products if not can_used(company, x)]
    produced_products_universe = fz.product_universes(company, produced_products)
    produced_products_ant = fz.product_membresy_functions(produced_products_universe, produced_products, True)
    produced_products_con = fz.product_membresy_functions(produced_products_universe, produced_products, False)
    sell_product_rules = []
    buy_product_rules = []
    produce_rules = []
    i = 0
    for product in produced_products_ant:
        priority = fz.ctrl.Consequent(priority_universe, f'sell {produced_products[i].name}')
        priority_membresy_sell.append(priority)
        priority.automf(5)
        sell_product_rules.append(fz.ctrl.rule(product['poor'] ,priority['poor']))
        sell_product_rules.append(fz.ctrl.rule(product['mediocre'] ,priority['mediocre']))
        sell_product_rules.append(fz.ctrl.rule(product['average'] ,priority['average']))
        sell_product_rules.append(fz.ctrl.rule(product['decent'] ,priority['decent']))
        sell_product_rules.append(fz.ctrl.rule(product['good'] ,priority['good']))
        i += 1
    
def greedy_algorithm(company, state):
    node = Node(company,state,None,None,0,0)
    next_node = greedy(node)
    return next_node.action

def random_algorithm(company, state):
    node = Node(company,state,None,None,0,0)
    next_node = random_search(node)
    return next_node.action                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
