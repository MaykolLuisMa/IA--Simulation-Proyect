from search.Graph_Search_Algorhitms import uniform_cost_search, get_next_node, greedy, random_search
from search.Node import Node
from simulation.Company import Company
def get_company_action(company : Company, state):
    return company.algorthm(company, state)
    
def uniform_cost_search_algorithm(company, state):
    node = Node(company,state,None,None,0,0)
    goal_node = uniform_cost_search(node)
    next_node = get_next_node(node,goal_node)
    return next_node.action

def greedy_algorithm(company, state):
    node = Node(company,state,None,None,0,0)
    next_node = greedy(node)
    return next_node.action

def random_algorithm(company, state):
    node = Node(company,state,None,None,0,0)
    next_node = random_search(node)
    return next_node.action