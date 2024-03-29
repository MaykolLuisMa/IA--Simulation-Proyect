from typing import List, Dict, Tuple
from Company import Company ,Seller, Buyer, Global_Company
from Product import Personal, Product_in_sale, Product_to_buy , Marquet_Product_Dates, get_product_list
from Condition import Condition, compute_condition
from copy import deepcopy
from utils import normal_variation
import random

class Marquet:
    def __init__(self, global_seller : Seller, global_buyer : Buyer):
        self.sellers = [global_seller]
        self.buyers = [global_buyer]
        self.products = get_product_list()
        self.actions_value = 1
        self.personal = Personal()

    def add_seller(self,company : Company, in_sale : Product_in_sale):
        self.sellers.append(Seller(company,in_sale))
    def add_buyer(self,company : Company, to_buy : Product_to_buy):
        self.buyers.append(Buyer(company,to_buy)) 
        
    def order_sellers_by_product(self) -> Dict[int,List]:
        products_in_sale = {p.id:[] for p in self.products}
        for s in self.sellers:
            for pis in s.in_sale.values():
                products_in_sale[pis.product.id].append((pis,s.company))
        for i in products_in_sale:
            products_in_sale[i] = sorted(products_in_sale[i],key=lambda item : -item[0].price)
        return products_in_sale
 
    def order_buyers_by_product(self) -> Dict[int,List[Tuple[Product_to_buy,Company]]]:
        self.buyers = buyer_sort(self.buyers)
        products_to_buy = {p.id:[] for p in self.products}
        for s in self.buyers:
            for pis in s.to_buy.values():
                products_to_buy[pis.product.id].append((pis,s.company))
        return products_to_buy
    
    def get_past_seller_dates(self):
        """
        get price average and total of seller of every product
        """
        products_in_sale = {p.id:[Product_in_sale(p,0,0),0,0] for p in self.products}
        for s in self.sellers:
            for pis in s.in_sale.values():
                products_in_sale[pis.product.id][0].amount += pis.amount
                products_in_sale[pis.product.id][1] += pis.price
                products_in_sale[pis.product.id][2] += 1
        for p in products_in_sale:
            products_in_sale[p][0].price = products_in_sale[p][1]/products_in_sale[p][2]
        return {i:l[0] for i,l in products_in_sale.items()}
    
    def get_past_buyer_dates(self):
        """
        get total of seller of every product
        """
        products_to_buy = {p.id:Product_to_buy(p,0) for p in self.products}
        for s in self.buyers:
            for pis in s.to_buy.values():
                products_to_buy[pis.product.id].amount += pis.amount
        return {i:p for i,p in products_to_buy.items()}

    def get_market_products_dates(self):
        in_sale_dates = self.get_past_seller_dates()
        to_buy_dates = self.get_past_buyer_dates()
        global_seller = deepcopy(self.sellers[0])
        global_buyer = deepcopy(self.buyers[0])
        market_products_dates = []
        for id in global_seller.in_sale:
            demand = global_buyer.to_buy[id].amount,to_buy_dates[id].amount
            offert = global_seller.in_sale[id].amount,in_sale_dates[id].amount
            price = in_sale_dates[id].price * (to_buy_dates[id].amount/in_sale_dates[id].amount)
            product = global_seller.in_sale[id].product
            market_products_dates.append(Marquet_Product_Dates(product,price,offert,demand))
        return market_products_dates

    def compute_product_buy(self,product_id : int, psellers : List[Tuple[Product_in_sale,Company]], pbuyers : List[Tuple[Product_to_buy,Company]]):
        for i in range(len(pbuyers)):
            selled = min(psellers[0][0].amount,pbuyers[i][0].amount)
            if pbuyers[i][1].confirm_buy(Product_in_sale(psellers[0][0].product,psellers[0][0].price,selled)) == False:
                continue
            psellers[0][1].process_sell(Product_in_sale(psellers[0][0].product,psellers[0][0].price,selled))
            if selled == psellers[0][0].amount:
                psellers.remove(psellers[0])
                pbuyers[i][0].amount -= selled
                i -= 1
            else:
                psellers[0][0].amount -= selled
                
    def compute_all_buys(self):
        product_to_buy = self.order_buyers_by_product()
        product_in_sale = self.order_sellers_by_product()
        for p in product_to_buy:
            self.compute_product_buy(p,product_in_sale[p],product_to_buy[p])
        
    def ejecute_iteration(self, conditions : List[Condition]):
        market_products_dates = self.get_market_products_dates()
        self.compute_all_buys()
        self.set_global_marquet(market_products_dates,conditions)

    def set_global_marquet(self,market_products_dates : List[Marquet_Product_Dates], conditions : List[Condition]):
        compute_condition(market_products_dates,conditions)
        in_sale = []
        to_buy = [] 
        
        for p in market_products_dates:
            in_sale.append(Product_in_sale(p.product,normal_variation(p.price),p.external_marquet_offert))
            to_buy.append(Product_to_buy(p.product,p.external_marquet_demand))
        self.buyers = [Buyer(Global_Company(),to_buy)]
        self.sellers = [Seller(Global_Company(),in_sale)]

def set_global_in_sale(products : List[Product_in_sale], conditions : List[Condition]):
    in_sale = products
    for c in conditions:
        in_sale = c.get_product_in_sale(in_sale)

def buyer_sort(buyers : List[Buyer]) -> List[Buyer]:
    sorted_buyers = []
    copied_buyers = deepcopy(buyers)
    for i in range(len(buyers)):
        total = sum([buyer.company.staff_capacity for buyer in copied_buyers])
        capacities = [buyer.company.staff_capacity/total for buyer in copied_buyers]
        buyer = random.choices(copied_buyers,capacities,k=1)[0]
        sorted_buyers.append(buyer)
        copied_buyers.remove(buyer)
    return sorted_buyers
