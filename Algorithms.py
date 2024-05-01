from search.Graph_Search_Algorhitms import uniform_cost_search, get_next_node, random_search, pib_greedy, coin_greedy
from search.Node import Node
from simulation.Company import Company
def get_company_action(company : Company, state):
    return company.algorthm(company, state)
    
def uniform_cost_search_algorithm(company, state):
    node = Node(company,state,None,None,0,0)
    goal_node = uniform_cost_search(node)
    next_node = get_next_node(node,goal_node)
    return next_node.action

def pib_greedy_algorithm(company, state):
    return pib_greedy(company, state)

def coin_greedy_algorithm(company, state):
    return coin_greedy(company, state)

def random_algorithm(company, state):
    node = Node(company,state,None,None,0,0)
    next_node = random_search(node)
    return next_node.action