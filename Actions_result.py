from Posible_Actions import Action
from State import State, next_state
from Company import Company
from Node import Node
import Posible_Actions
from copy import deepcopy
def action_result(action : Action):
    action.state = next_state(action.state,[action])
    #print(f"valid{action.company.id in action.state.companies}")
    return action.company, action.state

def expand_node(node_to_expand : Node):
    node = deepcopy(node_to_expand)
    for action in Posible_Actions.determinate_posible_actions(node.company,node.state):
        c_company, c_state = action_result(action)
        cost = node.path_cost + Posible_Actions.action_cost(node.company,node.state,c_state,action)
        yield Node(c_company,c_state,node_to_expand,action,cost,node_to_expand.deep+1)

