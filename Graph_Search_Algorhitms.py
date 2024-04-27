import utils
from Actions_result import expand_node
from Node import Node, is_goal
from Company import get_company_value, nothing
from Posible_Actions import Action
import random
#def non_action(company,state):
#    return Action(nothing,company,state,[])

def greedy(initial_node : Node):
    nodes = []
    for node in expand_node(initial_node):
        if node.is_factible:
            nodes.append(node)
    return sorted(nodes, key=lambda n: -n.get_node_value(n))[0]

def limited_best_first_search(initial_node : Node,increment, limit, f):
    frontier = utils.PriorityQueue([initial_node],key=f)
    while frontier:
        node = frontier.pop()
        if is_goal(initial_node,node,increment):
            return node
        for child in expand_node(node):
            if node.is_factible:
                frontier.add(child)
    return greedy(initial_node)

def get_next_node(initial_node : Node, goal_node : Node):
     if goal_node.parent == initial_node:
        return goal_node
     else:
          return get_next_node(initial_node,goal_node.parent)



#def best_possible_growds(current_node : Node):
#    factory, ganance = current_node.state.get_best_potential_factory()
#    pass

#def h_hamming_modificate(initial_node : Node, current_node : Node, increment):
#    return 0
#    initial_value = get_company_value(initial_node.company,initial_node.state.market)
#    goal_value = initial_value*increment

def g(n : Node): return n.path_cost
def uniform_cost_search(initial_node):
    return limited_best_first_search(initial_node,1.2,50,g)

def random_search(initial_node : Node):
    nodes = []
    for node in expand_node(initial_node):
        if node.is_factible:
            nodes.append(node)
    return random.sample(nodes,k=1)[0]