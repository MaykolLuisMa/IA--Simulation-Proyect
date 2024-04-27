from Graph_Search_Algorhitms import uniform_cost_search, get_next_node, greedy, random_search
from Node import Node
from Company import Company
import fuzzy as fz
from State import State
import numpy as np

def get_company_action(company : Company, state):
    return company.algorthm(company, state)
 
def uniform_cost_search_algorithm(company, state):

    node = Node(company,state,None,None,0,0)
    goal_node = uniform_cost_search(node)
    next_node = get_next_node(node,goal_node)
    return next_node.action


def only_fuzzy_algorithm(company: Company, state: State):
    priority_universe = np.arange(0, 10, 1)
    
def greedy_algorithm(company, state):
    node = Node(company,state,None,None,0,0)
    next_node = greedy(node)
    return next_node.action

def random_algorithm(company, state):
    node = Node(company,state,None,None,0,0)
    next_node = random_search(node)
    return next_node.action
