from search.Posible_Actions import Action
from simulation.State import State, next_state
from simulation.Company import Company, get_company_value,  nothing
from search.Node import Node
import search.Posible_Actions as Posible_Actions
from copy import deepcopy


def non_action(company,state):
    return deepcopy(Action(nothing,company,state,[]))
def non_action_node(company, state, father_node):
    return Node(company,state,father_node,non_action(company,state),father_node.path_cost+Posible_Actions.action_cost(company,state,state,non_action)
                ,father_node.deep+1, True)
def action_result(action : Action):
    action.state, _ = next_state(action.state,[action])
    #print(f"valid{action.company.id in action.state.companies}")
    return action.company, action.state

def expand_node(node_to_expand : Node):
    node = deepcopy(node_to_expand)

    #yield non_action_node(node.company,node.state,node)
    for action in Posible_Actions.determinate_posible_actions(node.company,node.state) + [non_action(node.company,node.state)]:
        c_company, c_state = action_result(action)
        if (c_company.id not in c_state.companies) and (action.f != nothing):
            #print("Continue")
            #input()
            continue
        else:
            #print(f"Expansion {get_company_value(c_company,c_state.market)} {c_company.products}")
            pass
        cost = node.path_cost + Posible_Actions.action_cost(node.company,node.state,c_state,action)
        yield Node(c_company,c_state,node_to_expand,action,cost,node_to_expand.deep+1)
    