from nlp.Register import Register
from simulation.Initial_State import company_list, factory_list, product_list
from typing import List
from simulation.Company import build_factory, produce, buy, sell
from search.Posible_Actions import Action

def action_dictionary(action : Action):
    if action.f == build_factory:
        return f"construyò una nueva industria de tipo {action.args[0].name}"
    if action.f == produce:
        return f"procesò " + generate_list([f"{p.amount} unidades de {p.product.name}" for p in action.args[0]])
    if action.f == buy:
        return f"vendiò " + generate_list([f"{p.amount} unidades de {p.product.name}" for p in action.args[0]])
    if action.f == sell:
        return f"comprò " + generate_list([f"{p.amount} unidades de {p.product.name} a ${p.price}" for p in action.args[0]])
    
def build_informs(register: Register):
    total_inform = ""
    total_inform += company_inform()
    total_inform += factory_inform()
    total_inform += product_inform()
    for i in range(len(register)):
        total_inform += iteration_inform(register,i)
    return total_inform

def iteration_inform(register : Register, i):
    inform = f"La semana {i+1}:\n La inflaciòn fue del {register.inflation[i]}.\n"
    for reg in register.companies_registers.values():
        inform += f"La compañìa {reg.name} tuvo un valor estimado de ${reg.value[i]}. "
        inform += "Dicha compañìa " + action_dictionary(reg.actions[i])
        inform += "\n"
    return inform



def generate_list(list : List[str]):
    final_str = ""
    for i,word in enumerate(list):
        final_str += word
        if i == len(list)-1:
            final_str += "."
        else:
            final_str += ", "
    return final_str 

def company_inform():
    inform = "Las compañìas activas inicalmente son "
    companies_names = [corp.name for corp in company_list]
    inform += generate_list(companies_names)
    inform += "\n"
    return inform
    
def factory_inform():
    inform = "Los tipos de idustrias son "
    factories_names = [fact.name for fact in factory_list]
    inform += generate_list(factories_names)
    inform += "\n"
    return inform

def product_inform():
    inform = "Los tipos de productos son "
    factories_names = [p.name for p in product_list]
    inform += generate_list(factories_names)
    inform += "\n"
    return inform