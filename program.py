from typing import List
from Company import Company
from Marquet import Marquet
from Agreement import Agreement
from Loan import Loan
from Condition import Condition
class Simulation:
    def __init__(self, companies : List[Company], marquet : Marquet, factories, agreements : List[Agreement],loans : List[Loan], conditions : List[Condition]):
        self.companies = companies
        self.marquet = marquet
        self.factories = factories
        self.agreements = agreements
        self.loans = loans
        self.conditions = conditions
    def ejecution(self,duration_limit = 10):
        for i in range(duration_limit):
            self.print_products()
            for c in self.companies:
                cost = c.get_operation_cost(self.marquet.personal)
                c.add_products[-cost]
            for a in self.agreements:
                a.duration += 1
                if(a.is_over()):
                    self.agreements.remove(a)
                else:
                    a.compute_agreement()
            for l in self.loans:
                l.duration += 1
                if l.is_over():
                    l.client.pay_loan_indemnization(l)
                    self.loans.remove(l)
            for c in self.companies:
                pass
            self.marquet.ejecute_iteration(self.conditions)

    def print_products(self):
        print("___Dates___")
        print("Sellers:")
        for seller in self.marquet.sellers:
            print(seller.company.name)
            for p in seller.in_sale.values():
                    print(f"{p.product.name}: {p.amount} units in sale, to ${p.price}")
            print("_____")
        print("_____________________________________________")
        print("Buyers:")
        for buyer in self.marquet.buyers:
            print(buyer.company.name)
            for p in buyer.to_buy.values():
                print(f"{p.product.name}: {p.amount} units to buy")
            print("_____")
        print("_____________________________________________")
    