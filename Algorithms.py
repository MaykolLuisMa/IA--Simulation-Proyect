from Graph_Search_Algorhitms import astar_search, get_next_node
from Node import Node
from Company import Company
import fuzzy as fz
from State import State
import numpy as np

def get_company_action(company : Company, state):
    return company.algorthm(company, state)
def a_star_algorithm(company, state):
    node = Node(company,state,None,None,0,0)
    goal_node = astar_search(node)
    next_node = get_next_node(node,goal_node)
    return next_node.action

def only_fuzzy_algorithm(company: Company, state: State):
    priority_universe = np.arange(0, 10, 1)
    