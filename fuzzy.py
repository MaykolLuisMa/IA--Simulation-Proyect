import skfuzzy as fuzzy
from skfuzzy import control as ctrl
from simulation.Company import get_company_storage_limit, Company, sell
import numpy as np
from simulation.State import State
from simulation.Product import Product
from search.Posible_Actions import Action

def product_universe(company, product: Product):
    max = get_company_storage_limit(company=company, product=product)
    return np.arange(0, max.amount+5, 0.1)
def product_universes(company, products: list[Product]):
    universes = {}
    for product in products:
        universes[product.id] = product_universe(company, product)
    return universes

def capital_universe(company: Company, state: State, factor = 100):
    max = company.get_operation_cost(state.market.get_inflation_factor())*factor if company.get_operation_cost(state.market.get_inflation_factor())*factor > company.coin else company.coin
    return np.arange(0, max+1, 1)

def price_univrerse(product: Product, state: State, factor = 2):
    max = state.market.get_global_seller().in_sale.get(product_id=product.id)*factor
    return np.arange(0, max+1, 0.1)

def product_membresy_func(universe, product: Product, Ant: bool):
    fuzzy_set = ctrl.Antecedent(universe, product.id) if Ant else ctrl.Consequent(universe, product.id)
    fuzzy_set.automf(5)
    return fuzzy_set
def product_membresy_functions(universes: dict, products: list[Product], Ant: bool):
    fuzzy_sets = {}
    for product in products:
        fuzzy_sets[product.id] = product_membresy_func(universes[product.id], product, Ant)
    return fuzzy_sets


def money_membresy_func(universe, Ant: bool):
    fuzzy_set = ctrl.Antecedent(universe, "money")
    fuzzy_set.automf(5)
    return fuzzy_set
def materia_prima_rules(universes: dict, membresy_func):
    set = list(universes.items())
    final_set = set[0][1][membresy_func]
    for uni in universes:
        final_set = final_set & universes[uni][membresy_func]
    return final_set 
def execute_action(actions: dict, company, state):
    diccionario = dict(sorted(actions.items(), key=lambda item: item[1][0], reverse= True))
    for dic in diccionario:
        return Action(diccionario[dic][1][0], company, state, diccionario[dic][1][1])
def build_rules(lm_input: list, company, state):
    antecedent = lm_input[:-2]
    consecuent = lm_input[-1]
    priority = {}
    ant_universes = {}
    ant_membresy = {}
    all_products: list[Product] = [x.product for x in company.products]
    all_products_universe = product_universes(company, all_products)
    all_products_mem = product_membresy_func_trian(all_products_universe, all_products, True, 'mucho')
    all_products_mem_comp = product_membresy_func(all_products_universe, all_products, True, 'poco')
    ant_set = []
    #inp = 
    for input in lm_input[1:]:
        inp =  materia_prima_rules([])  


def product_membresy_func_trian(universe, product: Product, Ant: bool, membresy):
    fuzzy_set = ctrl.Antecedent(universe, product.id) if Ant else ctrl.Consequent(universe, product.id)
    fuzzy_set[membresy] = fuzzy.trimf(universe, [0, universe[-1], universe[-1]]) if membresy == 'mucho' else fuzzy.trimf(universe, [0, 0, universe[-1]])
    return fuzzy_set
def product_membresy_functions_trian(universes: dict, products: list[Product], Ant: bool, membresy):
    fuzzy_sets = {}
    for product in products:
        fuzzy_sets[product.id] = product_membresy_func_trian(universes[product.id], product, Ant, membresy)
    return fuzzy_sets 