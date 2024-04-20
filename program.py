from typing import List
from Company import Company, get_company_value
from Market import Market
from Agreement import Agreement
from Loan import Loan
from Condition import Condition
from State import State, next_state
from Register import Register
from Node import Node
from Graph_Search_Algorhitms import astar_search
from Posible_Actions import Action
from Initial_State import initial_state

class Simulation:
    def __init__(self, inicial_state : State):
        self.state = inicial_state
        self.last_iteration_dates = []
        self.register = Register(self.state.companies.values())

    def ejecution(self,duration_limit = 10):
        for i in range(duration_limit):
            inflation_factor = self.state.market.get_inflation_factor()
            self.register.inflation.append(inflation_factor)
            
            actions = []
            for corp in self.state.companies.values():
                self.register.companies_registers[corp.id].value.append(get_company_value(corp,self.state.market))
                node = Node(corp,self.state,None,None,0,0)
                next_node = astar_search(node)
                print(next_node.action)
                self.register.companies_registers[corp.id].actions.append(next_node.action)
                actions.append(next_node.action)
            for i in self.state.companies[0].factories.items():
                print(f"Factoires {i}")
            self.state = next_state(self.state,actions)

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
for corp in sim.register.companies_registers:
    for i in range(len(sim.register.companies_registers[corp])):
        print(f"Value: {sim.register.companies_registers[corp].value[i]}")
        print(f"Action: {sim.register.companies_registers[corp].actions[i]}")