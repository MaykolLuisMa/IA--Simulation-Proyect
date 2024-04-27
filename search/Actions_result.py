from search.Posible_Actions import Action
from simulation.State import State, next_state
from simulation.Company import Company
from search.Node import Node
import search.Posible_Actions as Posible_Actions
from copy import deepcopy
def action_result(action : Action):
    action.state = next_state(action.state,[action])
    #print(f"valid{action.company.id in action.state.companies}")
    return action.company, action.state

def expand_node(node_to_expand : Node):
    node = deepcopy(node_to_expand)
    for action in Posible_Actions.determinate_posible_actions(node.company,node.state):
        c_company, c_state = action_result(action)
        if c_company.id not in c_state.companies:
            continue
        else:
            print(f"Expansion {c_company.coin} {c_company.products}")
        cost = node.path_cost + Posible_Actions.action_cost(node.company,node.state,c_state,action)
        yield Node(c_company,c_state,node_to_expand,action,cost,node_to_expand.deep+1)

