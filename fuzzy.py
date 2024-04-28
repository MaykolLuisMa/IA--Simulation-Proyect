import skfuzzy as fuzzy
from skfuzzy import control as ctrl
from Company import get_company_storage_limit
import numpy as np
from Company import Company
from State import State
from Product import Product

def product_universe(company, product: Product):
    max = get_company_storage_limit(company=company, product=product)
    return np.arange(0, max, 1)  
def capital_universe(company: Company, state: State, factor = 10):
    max = company.get_operation_cost(state.market.get_inflation_factor())*factor
    return np.arange(0, max, 1)
def price_univrerse(product: Product, state: State, factor = 2):
    max = state.market.get_global_seller().in_sale.get(product_id=product.id)*factor
    return np.arange(0, max, 1)

def product_membresy_func(universe, product: Product, Ant: bool):
    fuzzy_set = ctrl.Antecedent(universe, product.name) if Ant else ctrl.Consequent(universe, product.name)
    fuzzy_set.automf(5)
    return fuzzy_set

def money_membresy_func(universe, Ant: bool):
    fuzzy_set = ctrl.Antecedent(universe, "money")
    fuzzy_set.automf(5)
    return fuzzy_set
