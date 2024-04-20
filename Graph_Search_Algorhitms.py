import utils
from Actions_result import expand_node
from Node import Node, is_goal
from Company import get_company_value
from Posible_Actions import Action
import numpy as np
def non_action(company,state):
    return Action(None,company,state,None)

def best_first_tree_search(inicial_node : Node, f):
    frontier = utils.PriorityQueue([inicial_node],key=f)
    last = inicial_node

    nodes = []#provisional
    while frontier:
        node = frontier.pop()
        #last = node
        if is_goal(inicial_node,node):
            print("return")
            return node
        for child in expand_node(node):
            frontier.add(child)
            nodes.append(child)
        return nodes[np.random.randint(0,len(nodes))]
    non = non_action(last.company,last.state)
    return Node(last.company,last.state,None,non,0,0,0)
def get_next_node(current_node : Node, goal_node : Node):
     if goal_node.parent == current_node:
        return goal_node
     else:
          return get_next_node(current_node,goal_node.parent)
     
def g(n : Node): return n.path_cost

def astar_search(initial_node, h=lambda n:0):
    return best_first_tree_search(initial_node, f=lambda n: g(n) + h(n))