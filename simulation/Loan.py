from simulation.Factory import Factory
from typing import Dict
class Loan:
    def __init__(self, bank, client, coin, interest, duration_limit, guarantee : Dict[Factory,int]):
        self.bank = bank
        self.client = client
        self.coin = coin
        self.interest = interest
        self.duration_limit = duration_limit
        self.guarantee = guarantee
        self.duration = 0        
    def is_over(self):
        return self.duration >= self.duration_limit

