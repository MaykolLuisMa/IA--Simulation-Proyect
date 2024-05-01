import fuzzy as fz
import numpy as np

from search.Graph_Search_Algorhitms import uniform_cost_search, get_next_node, greedy, random_search
from search.Node import Node
from search.Actions_result import Action
from simulation.Company import Company, can_produce, can_used, sell, build_factory, buy, produce
from simulation.State import State
from simulation.Product import Product
from simulation.Factory import Factory


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
    priority_membresy_produce = {}
    inputs = {}
    ## --- All procts --- ##
    all_products: list[Product] = company.products
    all_products_universe = fz.product_universes(company, all_products)
    all_products_ant = fz.product_membresy_functions(all_products_universe, all_products, True)

    ## --- produced products --- ##
    produced_products: list[Product] = [x for x in company.products if not can_used(company, x)]
    produced_products_ant =  {id: all_products_ant[id] for id in [objeto.id for objeto in produced_products]}               #fz.product_membresy_functions(produced_products_universe, produced_products, True)
    
    ## --- raw material --- ##
    raw_material: list[Product] = [x for x in company.products if not can_produce(company, x)]
    raw_material_ant = {id: all_products_ant[id] for id in [objeto.id for objeto in raw_material]}     #fz.product_membresy_functions(raw_material_universe, raw_material, True)

    ## --- produccion products --- ##
    production_products: list[Product] = [x for x in company.products if can_produce(company, x)]
    production_products_ant = {id: all_products_ant[id] for id in [objeto.id for objeto in production_products]}

    sell_product_rules = []
    buy_product_rules = []
    produce_rules = []
    
    ### ------ selling rules ------- ###
    for product in produced_products:
        priority = fz.ctrl.Consequent(priority_universe, f'sell {product.id}')
        priority_membresy_sell[f'sell {product.id}'] = priority
        #inputs[product.id] = 
        priority.automf(5)
        sell_product_rules.append(fz.ctrl.rule(produced_products_ant[product.id]['poor'] ,priority['poor']))
        sell_product_rules.append(fz.ctrl.rule(produced_products_ant[product.id]['mediocre'] ,priority['mediocre']))
        sell_product_rules.append(fz.ctrl.rule(produced_products_ant[product.id]['average'] ,priority['average']))
        sell_product_rules.append(fz.ctrl.rule(produced_products_ant[product.id]['decent'] ,priority['decent']))
        sell_product_rules.append(fz.ctrl.rule(produced_products_ant[product.id]['good'] ,priority['good']))

    ### ------ buying rules ------ ###
    for product in raw_material:
        priority = fz.ctrl.Consequent(priority_universe, f'buy {product.id}')
        priority_membresy_buy[f'buy {product.id}'] = priority
        #inputs[product.id] = 
        priority.automf(5)
        buy_product_rules.append(fz.ctrl.rule(raw_material_ant[product.id]['poor'] ,priority['poor']))
        buy_product_rules.append(fz.ctrl.rule(raw_material_ant[product.id]['mediocre'] ,priority['mediocre']))
        buy_product_rules.append(fz.ctrl.rule(raw_material_ant[product.id]['average'] ,priority['average']))
        buy_product_rules.append(fz.ctrl.rule(raw_material_ant[product.id]['decent'] ,priority['decent']))
        buy_product_rules.append(fz.ctrl.rule(raw_material_ant[product.id]['good'] ,priority['good']))
    
    ### ------ production rules ------ ###
    for product in production_products:
        priority = fz.ctrl.Consequent(priority_universe, f'produce {product.id}')
        priority_membresy_buy[f'buy {product.id}'] = priority
        factory: Factory = [x for x in state.factories if x.produced_products[0].id == product.id]
        raw_mat_ant = {id: all_products_ant[id] for id in [x.id for x in all_products if x.id in factory.necessary_products] }
        produce_rules.append(fz.materia_prima_rules(raw_mat_ant, 'poor') & all_products_ant["good"], priority['poor'])
        produce_rules.append(fz.materia_prima_rules(raw_mat_ant, 'mediocre') & all_products_ant["decent"], priority['mediocre'])
        produce_rules.append(fz.materia_prima_rules(raw_mat_ant, 'average') & all_products_ant["average"], priority['average'])
        produce_rules.append(fz.materia_prima_rules(raw_mat_ant, 'decent') & all_products_ant["mediocre"], priority['decent'])
        produce_rules.append(fz.materia_prima_rules(raw_mat_ant, 'good') & all_products_ant["poor"], priority['good'])


def greedy_algorithm(company, state):
    node = Node(company,state,None,None,0,0)
    next_node = greedy(node)
    return next_node.action

def random_algorithm(company, state):
    node = Node(company,state,None,None,0,0)
    next_node = random_search(node)
    return next_node.action                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
