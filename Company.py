from typing import List, Dict, Tuple
from Product import Personal,AccountedProduct, Product_in_sale, add_products, ProductCollection
from Factory import Factory, calculate_build_cost, calculate_operation_cost, produce_for_all_factories
from Loan import Loan
import math
import utils
class Company:
    def __init__(self, id : int, name : str, coin : float, products : ProductCollection, factories : Dict, basic_operation_cost : float, staff_capacity = 1):
        self.id = id
        self.name = name
        self.coin = coin
        self.products = products
        self.factories = factories
        self.staff_capacity = staff_capacity
        self.basic_operation_cost = basic_operation_cost
    
    def is_global_company():
        return False
    
    def get_operation_cost(self,personal,inflation_factor):
        cost = (self.basic_operation_cost*4/10)+((self.basic_operation_cost*6/10)*(personal.basic_price/10))*self.staff_capacity
        cost += sum([calculate_operation_cost(f_key,personal,self.factories)*self.factories[f_key] for f_key in self.factories])
        return cost*inflation_factor
    
    def process_sell(self, product : Product_in_sale):
        self.products.extract(product,product.amount) 
        self.coin += product.price
    
    def process_buy(self, product : Product_in_sale):
        self.products.append(product.product,product.amount)
        self.coin -= product.price
    
    def confirm_buy(self, market, product : Product_in_sale) -> bool:
        self.process_buy(product)
        return True, product.amount

    def add_products(self, products : ProductCollection):
        new_products = add_products(self.products, products)
        is_valid = new_products.is_positive()
        if is_valid:
             self.products = new_products
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
        self.staff_capacity += 1
    
class Seller:
    def __init__(self, company : Company, in_sale : ProductCollection):
        self.company = company
        self.in_sale = in_sale

class Buyer:
    def __init__(self, company : Company, to_buy : ProductCollection):
        self.company = company
        self.to_buy = to_buy

class Global_Company(Company):
    def __init__(self, id = -1, name = "Global Company", coin = 0, products = [], factories = {}, staff_capacity=1):
        super().__init__(id, name, coin, products, factories, staff_capacity)
    
    def confirm_buy(self, market, product: Product_in_sale) -> bool:
        global_seller = market.get_global_seller()
        global_price = global_seller.in_sale.get(product.product.id).price
        buy_price = product.price
        porcent = utils.get_porcent(global_price,buy_price)
        if porcent <= 1:
            return True,product.amount
        else:
            buy_porcent = 1-(porcent-1)
            to_buy = product.amount*buy_porcent
            return to_buy>0,to_buy 
    def process_sell(self, product: Product_in_sale):
        pass
    def is_global_company(self):
        return True
    


def get_company_value(corp : Company, market):
    val = 0
    val += corp.coin*market.get_inflation_factor()
    val += sum([f.building_cost for f in corp.factories])
    val += sum([p.product.basic_price for p in corp.products])
    val += corp.staff_capacity*market.personal.basic_price
    return val

#______________________________________________________________________________
def sell(company : Company, state, products : ProductCollection):
        state.market.add_seller(company, products)

def buy(company, state, products : ProductCollection):
        state.market.add_buyer(company, products)

def build_factory(company : Company,state, factory : Factory):
        cost = calculate_build_cost(factory, company.factories, state.market.inflation_factor)
        company.add_products(ProductCollection([],cost))
        company.add_factory(factory)

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

def produce(self : Company,state ,products : ProductCollection, factory : Tuple[Factory,int]):
        necesary, produced = produce_for_all_factories(products,factory)
        self.add_products(necesary)
        self.add_products(produced)

def propose_agreement(company1, state, company2, agreement):
        if company1.evaluate_agreement(agreement):
            state.agreements.append(agreement)

def pay_loan(company,state, loan : Loan):
        loan.bank.add_products([loan.coin])
        company.add_products([-loan.coin])
        state.loans.remove(loan)