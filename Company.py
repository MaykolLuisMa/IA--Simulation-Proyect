from typing import List, Dict, Tuple
from Product import Personal,AccountedProduct, Product_in_sale, add_products, ProductCollection
from Factory import Factory, calculate_build_cost, calculate_operation_cost, produce_for_all_factories
from Loan import Loan
import math
import utils
class Company:
    def __init__(self, id : int, name : str, coin : float, products : ProductCollection, factories : Dict, basic_operation_cost : float,algorithm, staff_capacity = 1):
        self.id = id
        self.name = name
        self.coin = coin
        self.products = products
        self.factories = factories
        self.staff_capacity = staff_capacity
        self.basic_operation_cost = basic_operation_cost
        self.algorthm = algorithm
    def __eq__(self,other):
        return self.id == other.id
    def is_global_company(self):
        return False
    
    def get_operation_cost(self,inflation_factor):
        cost = self.basic_operation_cost*self.staff_capacity
        cost += sum([calculate_operation_cost(f_key,inflation_factor,self.factories)*self.factories[f_key] for f_key in self.factories])
        return cost
    
    def process_sell(self, product : Product_in_sale):
        #print("Process sell company method")
        self.products.extract(product.product,product.amount) 
        self.coin += product.get_total_price()
    
    def process_buy(self, product : Product_in_sale):
        #print("Process buy")
        #print(f"Current products: {[p.amount for p in self.products]}")
        #print(f"Add amount {product.amount}")
        self.products.append(product.product,product.amount)
        #print(f"New products: {[p.amount for p in self.products]}")
        self.coin -= product.get_total_price()
    
    def confirm_buy(self, market, product : Product_in_sale) -> bool:
        self.process_buy(product)
        return True, product.amount

    def add_products(self, products : ProductCollection):
        self.products.coin = self.coin
        new_products = add_products(self.products, products)
        is_valid = new_products.is_positive()
        if is_valid:
             self.coin = new_products.coin
             self.products = new_products
        else:
             print("No valid")
             print(new_products.coin)
             print([p.amount for p in new_products])
        return is_valid
    
    def evaluate_agreement(self, company, agreement) -> bool:
        pass
    
    def add_factory(company, factory):
        if factory in company.factories:
            company.factories[factory] += 1
        else:
            company.factories[factory] = 1  

    def evaluate_loan(self,loan) -> bool:
        pass

    def upgrade_staff_capacity(self,personal : Personal):
        self.add_products([-(personal.basic_price*math.pow(self.staff_capacity+1,2))])
        self.staff_capacity += 0.1
    
    
class Seller:
    def __init__(self, company : Company, in_sale : ProductCollection):
        self.company = company
        self.in_sale = in_sale

class Buyer:
    def __init__(self, company : Company, to_buy : ProductCollection):
        self.company = company
        self.to_buy = to_buy

class Global_Company(Company):
    def __init__(self, id = -1, name = "Global Company", coin = 0, products = [], factories = {},algorithm = None, staff_capacity=1):
        super().__init__(id, name, coin, products, factories, algorithm, staff_capacity)
    
    def confirm_buy(self, market, product: Product_in_sale) -> bool:
        #print("Process sell global company method")
        global_seller = market.get_global_seller()
        global_price = global_seller.in_sale.get(product.product.id).price
        buy_price = product.price
        
        porcent = buy_price/global_price
        max_porcent = utils.uniform_variation(0.90,1.0)
        if porcent <= 1:
            return True,int(product.amount*max_porcent)
        else:
            buy_porcent = max_porcent-(porcent-1)
            to_buy = product.amount*buy_porcent
            return to_buy>0,to_buy 
    
    def process_sell(self, product: Product_in_sale):
        pass
    def is_global_company(self):
        return True


def can_used(company : Company, product):
    for fact in company.factories:
        if product.id in [p.product.id for p in fact.necessary_products]:
            return True
    return False      
def get_company_value(corp : Company, market):
    val = 0
    val += corp.coin/market.get_inflation_factor()
    val += sum([f.building_cost*i for f,i in corp.factories.items()])
    val += sum([p.product.basic_price*p.amount for p in corp.products])
    val += corp.staff_capacity*market.personal.basic_price*market.inflation_factor
    return val


def get_company_storage_limit(company : Company, product = None):
    products = ProductCollection([])
    for f,i in company.factories.items():
        products = add_products(products,f.get_max_necessary(i))
        products = add_products(products,f.get_max_produced(i))
    if product == None:
        return products
    return products.get(product.id)
def get_company_free_space(company : Company, product = None):
    limits = get_company_storage_limit(company)
    for p in limits:
        current = 0 if company.products.get(p.product.id) == None else company.products.get(p.product.id).amount
        limits.get(p.product.id).amount -= current
    return limits 
#______________________________________________________________________________
def sell(company : Company, state, products : ProductCollection):
        state.market.add_seller(company, products)

def buy(company : Company, state, products : ProductCollection):
        free_space = get_company_free_space(company) 
        for p in products:
            products.get(p.product.id).amount = min(free_space.get(p.product.id).amount, p.amount)
        #print(f"add buyer {[p.amount for p in products]}")
        state.market.add_buyer(company, products)

def build_factory(company : Company,state, factory : Factory):
        cost = calculate_build_cost(factory, company.factories, state.market.inflation_factor)
        is_build = company.add_products(ProductCollection([],-cost))
        if is_build:
             company.add_factory(factory)
        return is_build
def ask_loan(company, state, loan):
        if loan.client.evaluate_loan():
            state.loans.append(loan)

def pay_loan_indemnization(company : Company, loan : Loan):
        for f in loan.guarantee:
            company.factories[f] -= loan.guarantee[f]
            for i in range(loan.guarantee[f]):
                loan.bank.add_factory(f)
            if company.factories[f] == 0:
                company.factories.pop(f)

def produce(company : Company,state ,products : ProductCollection, factory : Tuple[Factory,int]):
        #print(f"disponible {[p.amount for p in products]}")
        necesary, produced = produce_for_all_factories(products,factory)

        free_space = get_company_free_space(company)
        for p in produced:
            p.amount = min(p.amount,free_space.get(p.product.id).amount)
        #print(f"necesary {[p.amount for p in necesary]}")
        company.add_products(necesary)
        company.add_products(produced)

def propose_agreement(company1, state, company2, agreement):
        if company1.evaluate_agreement(agreement):
            state.agreements.append(agreement)

def nothing(company, state):
    pass
def pay_loan(company,state, loan : Loan):
        loan.bank.add_products([loan.coin])
        company.add_products([-loan.coin])
        state.loans.remove(loan)