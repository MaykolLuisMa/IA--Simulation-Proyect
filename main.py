#dependencias
from nlp.nlp import *
from typing import List
from simulation.Company import Company, get_company_value
from simulation.Market import Market
from simulation.Agreement import Agreement
from simulation.Loan import Loan
from simulation.Condition import Condition
from simulation.State import State, next_state
from nlp.Register import Register, is_over
from search.Node import Node
from search.Graph_Search_Algorhitms import get_next_node
from search.Posible_Actions import Action
from simulation.Initial_State import initial_state
from Algorithms import get_company_action
from nlp.Inform_Builder import build_informs
import os
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
            print(f"Week :{self.state.week}")
            for corp in self.state.companies.values():
                print(f"Company value: {get_company_value(corp,self.state.market)}")
                print(f"Company coin {corp.coin}")
                self.register.companies_registers[corp.id].value.append(get_company_value(corp,self.state.market))
                
                action = get_company_action(corp,self.state)
                print(f"Action: {action}")
                print(f"Company products {[(p.product.name, p.amount) for p in corp.products]}")

                for fact in corp.factories.items():
                    print(f"Factoires {fact}")    
                self.register.companies_registers[corp.id].actions.append(action)
                actions.append(action)
            for p in self.state.market.get_global_seller().in_sale:
                print(f"Market sell product {p.product.name} {p.amount} ${p.price}")
            for p in self.state.market.get_global_buyer().to_buy:
                print(f"Market buyer product {p.product.name} {p.amount}")
            self.state, deleted = next_state(self.state,actions)
            if len(self.state.companies.values()) == 0:
                break
            self.register.event.append("")
            for corp in deleted:
                corp[self.state.week] += is_over(corp)
#            input()

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

#visual
sim = Simulation(initial_state)
sim.ejecution()
print('')
input('Press "enter" to continue...')
os.system('clear')
inform = build_informs(sim.register)

while(True):
    query = input('Enter your query:\n')
    os.system('clear')
    print('Loading...')
    result = response_result(inform, query)
    os.system('clear')
    print('RESULTS:')
    print(result)
    print('')
    input('Press "enter" to make another query...\n')
    os.system('clear')
