
import fuzzy as fz
import numpy as np
import skfuzzy as skf
from skfuzzy import control as ctrl

from search.Graph_Search_Algorhitms import uniform_cost_search, get_next_node, random_search, pib_greedy, coin_greedy

from search.Node import Node
from search.Actions_result import Action
from simulation.Company import Company, can_produce, can_used, sell, build_factory, buy, produce, get_company_free_space, Buyer
from simulation.State import State
from simulation.Product import Product, ProductCollection, Product_in_sale, AccountedProduct
from simulation.Factory import Factory


def get_company_action(company : Company, state):
    return company.algorthm(company, state)
 
def uniform_cost_search_algorithm(company, state):

    node = Node(company,state,None,None,0,0)
    goal_node = uniform_cost_search(node)
    next_node = get_next_node(node,goal_node)
    return next_node.action

def only_fuzzy_algorithm(company: Company, state: State):
    
    priority_universe = np.arange(0, 11, 0.001)
    priority_membresy_sell = {}
    priority_membresy_buy = {}
    priority_membresy_produce = {}
    inputs = {}

    money_universe = fz.capital_universe(company, state, 10000)
    money_ant = fz.money_membresy_func(money_universe, True)
    ## --- All procts --- ##
    all_products: list[Product] = [x.product for x in company.products]
    all_products_universe = fz.product_universes(company, all_products)
    all_products_ant = fz.product_membresy_functions(all_products_universe, all_products, True)

    ## --- produced products --- ##
    produced_products: list[Product] = [x.product for x in company.products if not can_used(company, x.product)]
    produced_products_ant =  {id: all_products_ant[id] for id in [objeto.id for objeto in produced_products]}
    
    ## --- raw material --- ##
    raw_material: list[Product] = [x.product for x in company.products if not can_produce(company, x.product)]
    raw_material_ant = {id: all_products_ant[id] for id in [objeto.id for objeto in raw_material]}

    ## --- produccion products --- ##
    production_products: list[Product] = [x.product for x in company.products if can_produce(company, x.product)]

    ### args ###
    args = {}
    fact = company.factories
#############################\\\\\\\\\\-----------RULES-----------///////////###########################
    sell_product_rules = []
    buy_product_rules = []
    produce_rules = []
    build_factory_rules = []

    ### ------ selling rules ------- ###
    for product in produced_products:
        if len(fact) == 0: break
        priority = ctrl.Consequent(priority_universe, f'sell {product.id}')
        priority_membresy_sell[f'sell {product.id}'] = priority
        args[f'sell {product.id}'] = (sell, [ProductCollection([Product_in_sale(product, product.basic_price*state.market.get_inflation_factor(), company.products.get(product.id).amount)])])
        priority.automf(5)
        sell_product_rules.append(ctrl.Rule(produced_products_ant[product.id]['poor'] ,priority['poor']))
        sell_product_rules.append(ctrl.Rule(produced_products_ant[product.id]['mediocre'] ,priority['mediocre']))
        sell_product_rules.append(ctrl.Rule(produced_products_ant[product.id]['average'] ,priority['average']))
        sell_product_rules.append(ctrl.Rule(produced_products_ant[product.id]['decent'] ,priority['decent']))
        sell_product_rules.append(ctrl.Rule(produced_products_ant[product.id]['good'] ,priority['good']))


    ### ------ buying rules ------ ###
    for product in raw_material:
        if len(fact) == 0: break
        priority = ctrl.Consequent(priority_universe, f'buy {product.id}')
        priority_membresy_buy[f'buy {product.id}'] = priority
        args[f'buy {product.id}'] = (buy,[ProductCollection([AccountedProduct(product, get_company_free_space(company, product).amount)])])
        priority.automf(5)
        buy_product_rules.append(ctrl.Rule(raw_material_ant[product.id]['good'] ,priority['poor']))
        buy_product_rules.append(ctrl.Rule(raw_material_ant[product.id]['decent'] ,priority['mediocre']))
        buy_product_rules.append(ctrl.Rule(raw_material_ant[product.id]['average'] ,priority['average']))
        buy_product_rules.append(ctrl.Rule(raw_material_ant[product.id]['mediocre'] ,priority['decent']))
        buy_product_rules.append(ctrl.Rule(raw_material_ant[product.id]['poor'] ,priority['good']))
        
    ### ------ production rules ------ ###
    for product in production_products:
        if len(fact) == 0: break
        priority = ctrl.Consequent(priority_universe, f'produce {product.id}')
        priority_membresy_produce[f'produce {product.id}'] = priority
        priority.automf(5)
        factorys = [x for x in company.factories if x.produced_products.get(product.id) != None]
        factory = factorys[0]
        necesary = [ AccountedProduct(x, company.products.get(x.id).amount) for x in all_products if factory.necessary_products.get(x.id) != None]
        args[f'produce {product.id}'] = (produce ,[ProductCollection(necesary),(factory, len(factorys))])
        raw_mat_ant = {id: all_products_ant[id] for id in [x.id for x in all_products if factory.necessary_products.get(x.id) != None] }
        produce_rules.append(ctrl.Rule(fz.materia_prima_rules(raw_mat_ant, 'poor') , priority['poor']))
        produce_rules.append(ctrl.Rule(fz.materia_prima_rules(raw_mat_ant, 'mediocre') , priority['mediocre']))
        produce_rules.append(ctrl.Rule(fz.materia_prima_rules(raw_mat_ant, 'average') , priority['average']))
        produce_rules.append(ctrl.Rule(fz.materia_prima_rules(raw_mat_ant, 'decent') , priority['decent']))
        produce_rules.append(ctrl.Rule(fz.materia_prima_rules(raw_mat_ant, 'good') , priority['good']))

    ### ------ factory building rules ------ ###
    all_sim_products = []
    for pr in state.market.get_global_seller().in_sale:
        all_sim_products.append(pr)
    factory_products = []
    for factory_p in [x.produced_products for x in state.factories]:
        for prod in factory_p:
            factory_products.append(prod.product.id)
    max_valuable = [ x for x in all_sim_products if x.price == max([x.price for x in all_sim_products if x.product.id in factory_products])][0]
    fa = [x for x in state.factories if x.produced_products.get(max_valuable.product.id) != None]
    build_priority = ctrl.Consequent(priority_universe, 'build')
    build_priority.automf(5)
    priority_membresy_produce['build'] = build_priority
    args['build'] = (build_factory ,fa)
    build_factory_rules.append(ctrl.Rule(money_ant['good'], build_priority['good']))
    build_factory_rules.append(ctrl.Rule(money_ant['mediocre'], build_priority['mediocre']))
    build_factory_rules.append(ctrl.Rule(money_ant['average'], build_priority['average']))
    build_factory_rules.append(ctrl.Rule(money_ant['decent'], build_priority['decent']))
    build_factory_rules.append(ctrl.Rule(money_ant['poor'], build_priority['poor']))

####################\\\\\\\\\----------Control System building --------------//////////##################
    rules = buy_product_rules + sell_product_rules + produce_rules + build_factory_rules if len(fact) > 0 else [build_factory_rules]
    system = ctrl.ControlSystem(rules)


    for product in all_products:
        if len(fact) == 0: break 
        inn = company.products.get(product.id).amount
        inputs[product.id] = inn
    inputs['money'] = company.coin
    action_priority = ctrl.ControlSystemSimulation(system)
    for imp in inputs:
        try: action_priority.input[imp] = inputs[imp] 
        except: continue
    action_priority.compute()
    execute = {}
    for act in action_priority.output:
        execute[act] = (action_priority.output[act], args[act])
    return fz.execute_action(execute, company, state) 




def pib_greedy_algorithm(company, state):
    return pib_greedy(company, state)

def coin_greedy_algorithm(company, state):
    return coin_greedy(company, state)

def random_algorithm(company, state):
    node = Node(company,state,None,None,0,0)
    next_node = random_search(node)
    return next_node.action                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
