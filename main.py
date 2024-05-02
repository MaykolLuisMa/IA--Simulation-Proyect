#dependencias
from nlp.nlp import *
from typing import List
from simulation.Company import *
from simulation.Market import *
from simulation.Agreement import *
from simulation.Loan import *
from simulation.graphics import *
from simulation.Condition import *
from simulation.State import *
from nlp.Register import *
from search.Node import *
from search.Graph_Search_Algorhitms import *
from search.Posible_Actions import *
from simulation.Initial_State import *
from Algorithms import *
from nlp.Inform_Builder import *
import os
from utils import *
class Simulation:
    def __init__(self, inicial_state : State):
        self.state = inicial_state
        self.last_iteration_dates = []
        self.register = Register(self.state.companies.values())

    def ejecution(self):
      list_companies = list(self.state.companies.values()) #aceder a las empresas

      #simulacion
      while(True):
        companies = clone(list_companies) #clon de las empresas para no trabajar sobre la referencia directa
        duration_limit = None #duracion en semanas de la simlaion
        company = None #empresa seleccionada por el usuario
        control_system = []
        rules_x_company = {}
        
        for element in list_companies:
          rules_x_company[element.name] = 0
        
        os.system('clear')
        print('Below we show you a couple of companies. Select a company, after that, you can define some rules and aply to it')
        print('COMPANIES')
        
        for i in range(len(companies)):
          print(f'{i + 1}.{companies[i].name}')
          
        choice = input('Press "enter" to run simulation without choice\n')
          
        while(True):
          #si pulsa enter todas las empresas son greedy
          if choice == '':
              duration_limit = 1000
              break
          
          #verificar que ingreso un numero
          elif is_int(choice)[0]:
            if is_int(choice)[1] > 0 and is_int(choice)[1] <= len(companies):
              company = companies[is_int(choice)[1] - 1] #empres seleccionada por el usuario
              rules_x_company[company.name] += 1
              os.system('clear')
              query = input('Fine. Now, define some rules and a number of weeks in a natural lenguaje query. Enter your query and then press "enter" to continue:\n')
              
              while(True):
                tokens = clean_query(['oro', 'comida', 'agua', 'cemento'], query) #tokens que representan las keywords
                products = [token['value'] for token in tokens if token['type'] == 'product'] #obtener solo los productos
                
                try:
                  #respuesta del modelo a las reglas
                  rules = response_rules(query, show_list(products), 'mucho, poco', 'venta, produccion, compra, construccion') 
                  
                  for token in tokens:
                    if token['type'] == 'product':
                      token['priority'] = rules[token['value']]
                  
                  #agregamos la accion al final   
                  tokens.append({'value': rules['action'][0], 'type': 'action', 'priority': rules['action'][1]})  
                  control_system.append(build_rules(tokens, company, self.state)) 
                  break
                                     
                except:
                  query = input('Enter a valid query')
              
              #si hay empresas en la copia, entonces se puede escoger una para rulear
              if len(companies) > 0:
                if rules_x_company[company.name] == 4 and len(companies) == 1:
                  break
                
                handle_company = ''
                os.system('clear')
                handle_company = input('Put "si" if you want to keep handling or "no" to run simulation\n')
              
                while(True):
                  if(handle_company.lower().strip() != 'si' and handle_company.lower().strip() != 'no'):
                    handle_company = input('Ingress a valid option\n')

                  else: 
                    break
                
                #si marca que si vuelve al menu con las empresas disponibles              
                if handle_company.lower().strip() == 'si':
                  if rules_x_company[company.name] == 4:
                    companies.remove(company)
                    
                  os.system('clear')
                  print('Below we show you a couple of companies. Select a company, after that, you can define some rules and aply to it')
                  print('COMPANIES')

                  for i in range(len(companies)):
                    print(f'{i + 1}.{companies[i].name}')

                  choice = input('Press "enter" to run simulation without choice\n')
                  continue

                else:
                  break
              
              else:
                break
                    
            else:
              choice = input('Ingress a valid option\n')
          
          else:
            choice = input('Ingress a valid option\n')  
        
        #hacer que el usuario defina el tiempo 
        os.system('clear')
        duration_limit = input('Put the number of weeks that you want to take the simulation\n')
        
        while(True):
          #si ingreso un entero "n", corremos la simulacion "n" semanas 
          if(is_int(duration_limit)[0]):
            duration_limit = is_int(duration_limit)[1]
            break

          else:
            duration_limit = input('Ingress a valid option\n21')
        
        #imprimir las interacciones                        
        for i in range(duration_limit):
            inflation_factor = self.state.market.get_inflation_factor()
            self.register.inflation.append(inflation_factor)
            actions = []
            print(f"Week :{self.state.week}")
            for corp in self.state.companies.values():
                print(f"Company value: {get_company_value(corp,self.state.market)}")
                print(f"Company coin {corp.coin}")
                self.register.companies_registers[corp.id].value.append(get_company_value(corp,self.state.market))
                action = get_company_action(corp,self.state)
                print(f"Action: {action}")
                print(f"Company products {[(p.product.name, p.amount) for p in corp.products]}")
                for fact in corp.factories.items():
                    print(f"Factoires {fact}")    
                self.register.companies_registers[corp.id].actions.append(action)
                actions.append(action)
            for p in self.state.market.get_global_seller().in_sale:
                print(f"Market sell product {p.product.name} {p.amount} ${p.price}")
            for p in self.state.market.get_global_buyer().to_buy:
                print(f"Market buyer product {p.product.name} {p.amount}")
            self.state, deleted = next_state(self.state,actions)
            self.register.event.append("")
            for corp in deleted:
                corp[self.state.week] += is_over(corp)
        
        #si sigue simulando o termina
        print('')
        next = input('Press "enter" to keep simulating or write "leave" to finish simulation\n')
        
        if next == '':
            continue
        
        while(next.lower().strip() != 'leave'):
            next = input('Write "leave" to finish simulation\n')
            
        break
                    
    def print_products(self):
        print("___Dates___")
        print("Sellers:")
        for seller in self.market.sellers:
            print(seller.company.name)
            for p in seller.in_sale.values():
                    print(f"{p.product.name}: {p.amount} units in sale, to ${p.price}")
            print("_____")
        print("_____________________________________________")
        print("Buyers:")
        for buyer in self.market.buyers:
            print(buyer.company.name)
            for p in buyer.to_buy.values():
                print(f"{p.product.name}: {p.amount} units to buy")
            print("_____")
        print("_____________________________________________")

#visual
while(True):
  #menu de agregar empresas
  list_companies = list(initial_state.companies.values())
  os.system('clear')
  print('COMPANIES')

  for i in range(len(list_companies)):
    print(f'{i + 1}.{list_companies[i].name}')

  print('')
  query = input('Do you want to add another company?\n1.si\n2.no\n')

  while(True):
    if is_int(query)[0]:
      if is_int(query)[1] == 1 or is_int(query)[1] == 2:
        break
      
      else:
        query = input('Ingress a valid option\n')

    else:
      query = input('Ingress a valid option\n')

  if query == '1':
    os.system('clear')
    name = input('Ingress a none empty name\n')
    
    while(name == '' or name in [x.name for x in list_companies]):
      if name == '':
        name = input('Ingress a none empty name\n')
      
      else:
        name = input('Selected name already exists\n')
       
    initial_state.companies[len(initial_state.companies)] = Company(len(initial_state.companies), name,100000, ProductCollection([AccountedProduct(product_list[0],10),AccountedProduct(product_list[1],1000)]),{factory_list[0]:1},100,greedy_algorithm)
    continue 

  break

sim = Simulation(initial_state)

sim.ejecution()
#show(sim.register.inflation)
#for cr in sim.register.companies_registers.values():
#    show(cr.value)
os.system('clear')
inform = build_informs(sim.register)
query = input('Now, put some querys about the simulation.Enter your query\n')

while(True):  
  os.system('clear')
  print('Loading...')
  result = response_result(inform, query)
  os.system('clear')
  print('RESULTS:')
  print(result)
  print('')
  query = input('Press "enter" to make another query...\n')


