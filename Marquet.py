from typing import List
from Company import Seller, Buyer
class Marquet:
    def __init__(self, sellers : List[Seller], buyers : List[Buyer]):
        self.sellers = sellers
        self.buyers = buyers
