from Company import Company
from Market import Market
from Agreement import Agreement
from Loan import Loan
from Condition import Condition
from typing import List,Tuple
from copy import deepcopy
from Product import ProductCollection
class State:
    def __init__(self, companies : List[Company], market : Market, factories, agreements : List[Agreement],loans : List[Loan], conditions : List[Condition]):
        self.companies = {corp.id:corp for corp in companies}
        self.market = market
        self.factories = factories
        self.agreements = agreements
        self.loans = loans
        self.conditions = conditions

    def next_state(self,company_actions : List):
        next = self
        compute_agreements(next)
        compute_loans(next)
        compute_operation_cost(next)
        compute_company_actions(next, company_actions)
        next.market.ejecute_iteration(self.conditions)
        return self
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
    for corp in state.companies.values():
        cost = corp.get_operation_cost(state.market.personal,inflation_factor)
        corp.add_products(ProductCollection([],-cost))

def compute_company_actions(state : State, company_action : List):
    for act in company_action:
        act.state = state
        act.ejecute_action()
