import utils
from Actions_result import expand_node
from Node import Node, is_goal
from Company import get_company_value
from Posible_Actions import Action
import numpy as np

def non_action(company,state):
    return Action(None,company,state,None)


def best_first_tree_search(inicial_node : Node,increment, f):
    frontier = utils.PriorityQueue([inicial_node],key=f)
    last = inicial_node

    while frontier:
        node = frontier.pop()
        if is_goal(inicial_node,node,increment):
            return node
        for child in expand_node(node):
            frontier.add(child)
    
    non = non_action(last.company,last.state)
    return Node(last.company,last.state,None,non,0,0,0)

def get_next_node(current_node : Node, goal_node : Node):
     if goal_node.parent == current_node:
        return goal_node
     else:
          return get_next_node(current_node,goal_node.parent)
     
def g(n : Node): return n.path_cost

def best_possible_growds(current_node : Node):
    factory, ganance = current_node.state.get_best_potential_factory()
    pass




def h_hamming_modificate(initial_node : Node, current_node : Node, increment):
    initial_value = get_company_value(initial_node.company)
    goal_value = initial_value*increment

def astar_search(initial_node, h=h_hamming_modificate,increment = 1.2):
    return best_first_tree_search(initial_node,increment, f=lambda n: g(n) + h(initial_node,n,increment))