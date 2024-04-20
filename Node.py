import utils
from Company import get_company_value
from State import State
class Node:
    def __init__(self,company, state : State, parent, action, path_cost,deep):
        self.company=company
        self.state=state 
        self.parent=parent 
        self.action=action 
        self.path_cost=path_cost
        self.deep = deep
    
    def get_node_value(self):
        return get_company_value(self.company,self.state.market)
    
    def __lt__(self, other): return self.path_cost < other.path_cost

def is_goal(initial_node : Node, final_node : Node, increment = 1.1):
    initial_node_value = initial_node.get_node_value()
    final_node_value = final_node.get_node_value()
    
    
    print("initial")
    print(initial_node_value)
    print("final")
    print(final_node_value)
    print("_________________")
    return final_node_value/initial_node_value > increment
