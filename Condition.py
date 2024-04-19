from Product import market_Product_Dates
from typing import List
from utils import random_up, random_down
import numpy as np
class Condition:
    def modify_by_condition(self, products : List[market_Product_Dates]):
        pass
    def is_occurred(self):
        pass
class Adaptation_5_porcent(Condition):
    def modify_by_condition(self, products : List[market_Product_Dates]):
        for p in products:
            if p.general_offert > p.general_demand:
                p.external_market_offert = random_down(p.external_market_offert)
            else:
                p.external_market_offert = random_up(p.external_market_offert)
    def is_occurred(self):
        return super().is_occurred()

def compute_condition(products : List[market_Product_Dates], conditions : List[Condition]):
    for condition in conditions:
        condition.modify_by_condition(products)

class Hyerinflation(Condition):
    def __init__(self):
        self.is_active = False
        self.iteration = 0
        self.porcent = np.random.choice([self.brazil_dates(),self.venezuela_dates()])
    def is_occurred(self):
        if not self.is_active:
            self.is_active = np.random.randint(0,100) == 0

    def brazil_dates(self):
        porcent = [12.0, 14.1, 15.0, 20.1, 27.6, 25.9, 9.3, 4.5, 8.0, 11.2, 14.5, 15.9, 
                   19.1, 17.7, 18.2, 20.3, 19.5, 20.8, 21.5, 22.9, 25.8, 27.6, 28.0, 28.9,
                   36.6, 11.8, 4.2, 5.2, 12.8, 26.8, 37.9, 36.5, 38.9, 39.7, 44.3, 49.4, 
                   71.9, 71.7, 81.3, 11.3, 9,1, 9.0]
        return porcent
    def venezuela_dates(self):
        porcent = [19,20,16,17,18,21,26,34,36,46,57,85,84,80,67,80,110,128,125,223,233,148,144,142
                   ,192,54,18,45,31,25,34,65,24,21,36,33,65,22,21,80,15,20,55]
        return porcent
    def modify_by_condition(self, products : List[market_Product_Dates]):
        for p in products:
            p.price *= self.porcent[self.iteration]
        self.iteration+=1
        if self.iteration == len(self.porcent):
            self.is_active = False




