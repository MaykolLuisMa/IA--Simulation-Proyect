from typing import List, Dict, Tuple
from Product import Personal,Product_to_buy, Product_in_sale
from Factory import Factory, calculate_build_cost, calculate_operation_cost, produce
from Loan import Loan
import math
class Company:
    def __init__(self, id : int, name : str, coin : float, products : List[Product_to_buy], factories : Dict, basic_operation_cost : float, staff_capacity = 1):
        self.id = id
        self.name = name
        self.coin = coin
        self.products = {p.product.id:p for p in products}
        self.factories = factories
        self.staff_capacity = staff_capacity
        self.basic_operation_cost = basic_operation_cost
    def sell(self, marquet, products : List[Product_to_buy]):
        marquet.add_seller(self, products)

    def buy(self, marquet, products : List[Product_to_buy]):
        marquet.add_buyer(self,products)

    def build_factory(self, factory : Factory,actions):
        cost = calculate_build_cost(factory, self.factories, actions)
        if self.coin < cost:
            return
        self.coin -= cost
        self.add_factory(factory)
        
    def add_factory(self,factory):
        if factory in self.factories:
            self.factories[factory] += 1
        else:
            self.factories[factory] = 1    
    def produce(self, products : List[Product_to_buy], factory : Tuple[Factory,int]):
        necesary, produced = produce(products,factory)
        self.add_products(necesary)
        self.add_products(produced)

    def get_operation_cost(self,personal):
        cost = (self.basic_operation_cost*4/10)+((self.basic_operation_cost*6/10)*(personal.basic_cost/10))*self.staff_capacity
        cost += sum([calculate_operation_cost(f_key,personal,self.factories)*self.factories[f_key] for f_key in self.factories])
        return cost
    
    def process_sell(self, product : Product_in_sale):
        self.products[product.product.id].amount -= product.amount
        self.coin += product.price
    
    def process_buy(self, product : Product_in_sale):
        if product.product.id in self.products:
            self.products[product.product.id].amount += product.amount
        else:
            self.products[product.product.id].amount = Product_to_buy(product.product,product.amount)
        self.coin -= product.price
    
    def confirm_buy(self, product : Product_in_sale) -> bool:
        self.process_buy(product)
        return True

    def add_products(self, products : List):
        if any(self.products[p.product.id].amount < -p.amount for p in products[1:] if p.amount < 0):
            return False
        if type(products[0]) == float:
            self.coin += products[0]
            products = products[1:]
        for p in products:
            self.products[p.product.id].amount += p.amount
        return True
    def evaluate_agreement(self, company, agreement) -> bool:
        pass
    def propose_agreement(self, company, agreement):
        if company.evaluate_agreement(agreement):
            pass

    def ask_loan(self,loan,loans : List):
        if loan.client.evaluate_loan():
            loans.append(loan)
    
    def evaluate_loan(self,loan) -> bool:
        pass

    def pay_loan(self, loan : Loan, loans : List[Loan]):
        loan.bank.add_products([loan.coin])
        self.add_products([-loan.coin])
        loans.remove(loan)

    def pay_loan_indemnization(self, loan : Loan):
        for f in loan.guarantee:
            self.factories[f] -= loan.guarantee[f]
            for i in range(loan.guarantee[f]):
                loan.bank.add_factory(f)
            if self.factories[f] == 0:
                self.factories.pop(f)
    
    def upgrade_staff_capacity(self,personal : Personal):
        self.add_products([-(personal.basic_price*math.pow(self.staff_capacity+1,2))])
        self.staff_capacity += 1

    def actions(self,companies : List,personal : Personal,loans : List[Loan]):
        #upgrade_staff_capacity
        #ask_loan
        #pay_loan
        #propose_agreement
        #build_factory
        #produce
        #buy
        #sell
        pass
    
class Seller:
    def __init__(self, company : Company, in_sale : List[Product_in_sale]):
        self.company = company
        self.in_sale = {p.product.id:p for p in in_sale}

class Buyer:
    def __init__(self, company : Company, to_buy : List[Product_to_buy]):
        self.company = company
        self.to_buy = {p.product.id:p for p in to_buy}

class Global_Company(Company):
    def __init__(self, id = -1, name = "Global Company", coin = 0, products = [], factories = {}, staff_capacity=1):
        super().__init__(id, name, coin, products, factories, staff_capacity)
    def confirm_buy(self, product: Product_in_sale) -> bool:
        return True
    def process_sell(self, product: Product_in_sale):
        pass