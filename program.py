from typing import List
from Company import Company, get_company_value
from Market import Market
from Agreement import Agreement
from Loan import Loan
from Condition import Condition
from State import State, next_state
from Register import Register
from Node import Node
from Graph_Search_Algorhitms import get_next_node
from Posible_Actions import Action
from Initial_State import initial_state
from Algorithms import get_company_action
from Inform_Builder import build_informs
class Simulation:
    def __init__(self, inicial_state : State):
        self.state = inicial_state
        self.last_iteration_dates = []
        self.register = Register(self.state.companies.values())

    def ejecution(self,duration_limit = 100):
        for i in range(duration_limit):
            inflation_factor = self.state.market.get_inflation_factor()
            self.register.inflation.append(inflation_factor)
            
            actions = []
            for corp in self.state.companies.values():
                print(f"company value: {get_company_value(corp,self.state.market)}")
                print(f"company coin {corp.coin}")
                self.register.companies_registers[corp.id].value.append(get_company_value(corp,self.state.market))
                
                action = get_company_action(corp,self.state)
                print(f"Action: {action}")
                print(f"company products {[(p.product.name, p.amount) for p in corp.products]}")
                
                self.register.companies_registers[corp.id].actions.append(action)
                actions.append(action)
            if len(self.state.companies.values()) == 0:
                break
            for i in self.state.companies[0].factories.items():
                print(f"Factoires {i}")
            for p in self.state.market.get_global_seller().in_sale:
                print(f"Market sell product {p.product.name} {p.amount} ${p.price}")
            for p in self.state.market.get_global_buyer().to_buy:
                print(f"Market buyer product {p.product.name} {p.amount}")
            self.state = next_state(self.state,actions)
            input()

    def print_products(self):
        print("___Dates___")
        print("Sellers:")
        for seller in self.market.sellers:
            print(seller.company.name)
            for p in seller.in_sale.values():
                    print(f"{p.product.name}: {p.amount} units in sale, to ${p.price}")
            print("_____")
        print("_____________________________________________")
        print("Buyers:")
        for buyer in self.market.buyers:
            print(buyer.company.name)
            for p in buyer.to_buy.values():
                print(f"{p.product.name}: {p.amount} units to buy")
            print("_____")
        print("_____________________________________________")
    


sim = Simulation(initial_state)
sim.ejecution()
print("_____________________________________________________________________")
print("Informe:")
print(build_informs(sim.register))
