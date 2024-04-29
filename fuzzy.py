import skfuzzy as fuzzy
from skfuzzy import control as ctrl
from simulation.Company import get_company_storage_limit, Company
import numpy as np
from simulation.State import State
from simulation.Product import Product

def product_universe(company, product: Product):
    max = get_company_storage_limit(company=company, product=product)
    return np.arange(0, max, 1)
def product_universes(company, products: list[Product]):
    universes = {}
    for product in products:
        universes[product.id] = product_universe(company, product)
    return universes

def capital_universe(company: Company, state: State, factor = 10):
    max = company.get_operation_cost(state.market.get_inflation_factor())*factor
    return np.arange(0, max, 1)

def price_univrerse(product: Product, state: State, factor = 2):
    max = state.market.get_global_seller().in_sale.get(product_id=product.id)*factor
    return np.arange(0, max, 1)

def product_membresy_func(universe, product: Product, Ant: bool):
    fuzzy_set = ctrl.Antecedent(universe, product.name) if Ant else ctrl.Consequent(universe, product.id)
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
    final_set = universes.items[0][1] 
    for uni in universes:
        final_set = final_set & universes[uni]
    return final_set 