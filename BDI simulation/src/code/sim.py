#dependencias
from src.code.company import Company
from src.code.market import Market
from src.code.product import ProductMount
from src.nlp.nlp import response_result
from src.utils import pen
import os

#cliente final que compra los productos a las empresas
class Client:
  def __init__(self, companies: list[Company], clasification=None):
    self._pen = self._get_pen(clasification)
    self._last_week_transactions = {}
    
    for company in companies:
      self._last_week_transactions[company] = []
      
  #calcular la penalizacion que usa el cliente para comprar una cantidad de productos]
  def _get_pen(self, clasification) -> float:
    if clasification == 'abundance':
      return pen(min=0.5)
    
    if clasification == 'low':
      return pen(max=0.2)
    
    return pen()
  
  #accion de comprar
  def action(self, companies: list[Company]):
    self._last_week_transactions = {}
    result = ''
    
    for company in companies:
      self.last_week_transactions[company] = []
      
      for products in company.products:
        company.sell(ProductMount(products.product, int(products.mount * self._pen)))
        result += f'El cliente compro {int(products.mount * self._pen)} unidades del producto "{products.product.name}" a la empresa "{company.name}" por un precio de "{products.product.price} cada unidad".\n'
        self._last_week_transactions[company].append(ProductMount(products.product, int(products.mount * self._pen)))
    
    return result
  
  @property
  def last_week_transactions(self) -> dict[Company, list[ProductMount]]:
    return self._last_week_transactions
       
#simulacion
class Sim():
  def __init__(self):
    self._companies = []
    self._client = None
    self._weeks = None
    self._market = Market()
  
  #visual
  def sim(self):
    #numero de semanas
    self._weeks = self._set_weeks()
    
    #agregar las empresas
    os.system('cls')
    input('Excelent.Now, add a company...')
    
    while True:
      name = self._set_name()
      company = Company(name)
      
      for i in range(1, self._weeks + 1):
        self._handle_belief(company, i)
        
      self._companies.append(company)
      os.system('cls')
      advance = input('Press "add" to add another company in other case press "enter" to continue:\n')
      
      if advance.lower().strip() != 'add':
        break
      
    self._client = self._set_client()
    actions = self._execution()
    self._handle_querys(actions)
  
  #seleccionar el nombre de la empresa
  def _set_name(self) -> str:
    while True:
      os.system('cls')
      print('Add a name')
      name = input('Name: ')
      
      if len(list(filter(lambda x: x.name == name, self._companies))) != 0 or name == '':
        input('Invalid name or name already exists. Press "enter" to continue...')
        continue
      
      return name
          
  #crear al client
  def _set_client(self) -> Client:
    while True:
      os.system('cls')
      print('Now, select a clasification for the client')
      print('1.Abundance')
      print('2.Low')
      print('3.Random')
      option = input()
      
      try:
        if int(option) == 1:
          return Client(self._companies, 'abundance')
        
        if int(option) == 2:
          return Client(self._companies, 'low')
        
        if int(option) == 3:
          return Client(self._companies, )
        
        input('Ingress a valid option. Press "enter" to continue...')
        
      except:
        input('Ingress a number. Press "enter" to continue...')
        
  #determinar la duracion en semanas de la simulacion
  def _set_weeks(self) -> int:
    while True:
      os.system('cls')
      print('Welcome. Before start, add the numbers of weeks...')
      weeks = input('Weeks: ')
      
      try:
        if int(weeks) > 0:
          return int(weeks)

        input('Ingress number higher than 0. Press "enter" to continue')
        
      except:
        input('Ingress a valid number. Press "enter" to continue')
    
  #manejar los beliefs
  def _handle_belief(self, company: Company, week: int):
    while True:
      os.system('cls')
      print(f'Agregue reglas para la semana {week}:')
      print('1.El producto celular sera el de mejor productividad')
      print('2.El producto computadora sera el de mejor productvidad')
      print('3.No agregar regla')
      response = input()

      try:
        if int(response) == 1:
          company.add_belief('celular', week)

        elif int(response) == 2:
          company.add_belief('computadora', week)

        elif int(response) == 3:
          pass

        else:
          input('Ingress a valid option...')
          continue
        
        break

      except:
        input('Ingress a number...')
      
  #ejecutar la simulacion
  def _execution(self) -> str:
    os.system('cls')
    result = ''
    
    for i in range(self._weeks + 1):
      result += f'SEMANA {i}:\n'
      
      for company in self._companies:
        for sale in self._market.products:
          action = f'{company.action(sale.products, sale._factory, self._client.last_week_transactions[company], i)}.\n'
          
          if f'La empresa {company.name} quebro' in action:
            self._companies = list(filter(lambda x: x.name != company.name, self._companies))
          
          result += action
          break
        
      result += self._client.action(self._companies)
      result += '\n'
    
    for company in self._companies:
      result += f'El presupuesto final de la empresa "{company.name}" es de {company._presp} dolares.\n'
    
    result += '\n'
    input(result + 'Press "enter" to continue...')
    return result
        
  #encabezado del informe que se le enviara al modelo
  def _header_inform(self) -> str:
    result = f'En la simulacion se encuentran las siguiente empresas:\n'
    
    for company in self._companies:
      result += f'Empresa "{company.name}", dedicada a "{company.clasification}" con un presupuesto de {company._presp} dolares\n'
      
    result += 'Tambien se cuenta con un cliente final, cuya labor es comprar los productos de la empresa.'
    result += 'A continuacion te voy a enviar un informe de lo que sucedio cada semana.\n'
    return result
    
  #manejo de las querys
  def _handle_querys(self, inform: str):
    os.system('cls')
    inform = self._header_inform() + inform
    input('Now, put some querys about the simulation...\n')
    
    while(True):  
      query = input('query: ')
      os.system('cls')
      print('Loading...')
      result = response_result(inform, query)
      os.system('cls')
      print('RESULTS:')
      print(result)
      print('')
      input('Press "enter" to make another query...\n')
