from simulation.Company import Company
from simulation.Market import Market
from simulation.Agreement import Agreement
from simulation.Loan import Loan
from simulation.Condition import Condition
from typing import List,Tuple
from copy import deepcopy
from simulation.Product import ProductCollection
from simulation.Factory import Factory
class State:
    def __init__(self, companies : List[Company], market : Market, factories : List[Factory], agreements : List[Agreement],loans : List[Loan], conditions : List[Condition]):
        self.companies = {corp.id:corp for corp in companies}
        self.market = market
        self.factories = factories
        self.agreements = agreements
        self.loans = loans
        self.conditions = conditions
        self.week = 0
    def get_best_potential_factory(self):
        ganance = 0
        factory = None
        for fact in self.factories:
            inversion = 0
            result = 0
            for p in fact.necessary_products:
                inversion += p.amount*p.product.basic_price
            for p in fact.produced_products:
                result += p.amount*p.product.basic_price
            if result-inversion>ganance:
                ganance = result-inversion
                factory = fact
        return factory,ganance
def next_state(state : State,company_actions : List):
        compute_agreements(state)
        compute_loans(state)
        compute_company_actions(state, company_actions)
        deleted = compute_operation_cost(state)
        for s in state.market.sellers:
            #int(f"{s.company.is_global_company()}")
            for p in s.in_sale:
                #print(f"products: {p.product}")
                pass
        state.market.ejecute_iteration(state.conditions)
        state.week += 1
        return state, deleted

def compute_agreements(state : State):
    for a in state.agreements:
        a.duration += 1
        if(a.is_over()):
            state.agreements.remove(a)
        else:
            a.compute_agreement()

def compute_loans(state : State):
    for l in state.loans:
        l.duration += 1
        if l.is_over():
            l.client.pay_loan_indemnization(l)
            state.loans.remove(l)

def compute_operation_cost(state : State):
    inflation_factor = state.market.get_inflation_factor()
    to_delete = []
    for corp in state.companies.values():
        cost = corp.get_operation_cost(inflation_factor)
        is_soportable = corp.add_products(ProductCollection([],-cost))
        if is_soportable == False:
            to_delete.append(corp)            
    for corp in to_delete:
        state.companies.pop(corp.id,None)
    return to_delete
def compute_company_actions(state : State, company_action : List):
    #print(f"week {state.week}")
    for act in company_action:
  
        act.company = state.companies[act.company.id]
        act.state = state
        act.ejecute_action()
