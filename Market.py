from typing import List, Dict, Tuple
from Company import Company ,Seller, Buyer, Global_Company
from Product import Personal, Product_in_sale, AccountedProduct , market_Product_Dates, ProductCollection
from Condition import Condition, compute_condition
from copy import deepcopy
from utils import normal_variation, normalize_price
import random

class Market:
    def __init__(self, global_seller : Seller, global_buyer : Buyer,product_list):
        self.sellers = [global_seller]
        self.buyers = [global_buyer]
        self.products = product_list
        self.inflation_factor = 1
        self.personal = Personal()

    def add_seller(self,company : Company, in_sale : ProductCollection):
        self.sellers.append(Seller(company,in_sale))

    def add_buyer(self,company : Company, to_buy : ProductCollection):
        #print(f"To buy: {to_buy}")
        self.buyers.append(Buyer(company,to_buy)) 

    def get_inflation_factor(self):
        factors = [normalize_price(1,p.price,p.product.basic_price) for p in self.get_global_seller().in_sale]
        self.inflation_factor = sum(factors)/len(factors)
        return self.inflation_factor
    
    def order_sellers_by_product(self) -> Dict[int,List]:
        products_in_sale = {p.id:[] for p in self.products}
        for s in self.sellers:
            for pis in s.in_sale:
                products_in_sale[pis.product.id].append([pis,s.company])
        for p in products_in_sale:
            products_in_sale[p].reverse()
            
        for i in products_in_sale:
            products_in_sale[i]
            products_in_sale[i] = sorted(products_in_sale[i],key=lambda item : -item[0].price)
        return products_in_sale
    
    def get_global_seller(self):
        for s in self.sellers:
            if s.company.is_global_company():
                return s
    
    def get_global_buyer(self):
        for b in self.buyers:
            if b.company.is_global_company():
                return b
    def order_buyers_by_product(self) -> Dict[int,List[Tuple[AccountedProduct,Company]]]:
        self.buyers = buyer_sort(self.buyers)
        products_to_buy = {p.id:[] for p in self.products}
        for s in self.buyers:
            for pis in s.to_buy:
                products_to_buy[pis.product.id].append([pis,s.company])
        #for i in products_to_buy:
            #print(f"Num of buyers {len(products_to_buy[i])}")
        return products_to_buy
    
    def get_past_seller_dates(self):
        """
        get price average and total of seller of every product
        """
        products_in_sale = {p.id:[Product_in_sale(p,0,0),0,0] for p in self.products}
        for s in self.sellers:
            for pis in s.in_sale:
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
        products_to_buy = {p.id:AccountedProduct(p,0) for p in self.products}
        for s in self.buyers:
            for pis in s.to_buy:
                products_to_buy[pis.product.id].amount += pis.amount
        return {i:p for i,p in products_to_buy.items()}

    def get_market_products_dates(self):
        in_sale_dates = self.get_past_seller_dates()
        to_buy_dates = self.get_past_buyer_dates()
        global_seller = deepcopy(self.get_global_seller())
        global_buyer = deepcopy(self.get_global_buyer())
        market_products_dates = []
        for p in global_seller.in_sale:
            demand = global_buyer.to_buy.get(p.product.id).amount,to_buy_dates.get(p.product.id).amount
            offert = global_seller.in_sale.get(p.product.id).amount,in_sale_dates[p.product.id].amount
            price = in_sale_dates[p.product.id].price * (to_buy_dates[p.product.id].amount/max(1,in_sale_dates[p.product.id].amount))
            product = global_seller.in_sale.get(p.product.id).product
            market_products_dates.append(market_Product_Dates(product,price,offert,demand))
        return market_products_dates

    def compute_product_buy(self,product_id : int,
                             psellers : List[Tuple[Product_in_sale,Company]],
                             pbuyers : List[Tuple[AccountedProduct,Company]]):
        #print("Compute buy")
        for i in range(len(pbuyers)):
            if(len(psellers) == 0):
                break

            to_selled = min(psellers[0][0].amount, pbuyers[i][0].amount)

            buy_confirmation, to_selled = pbuyers[i][1].confirm_buy(self,Product_in_sale(psellers[0][0].product,psellers[0][0].price,to_selled))
            if  buy_confirmation == False:
                continue
            #print(f"Sellers number: {len(psellers)}")
            psellers[0][1].process_sell(Product_in_sale(psellers[0][0].product,psellers[0][0].price,to_selled))
            
            if to_selled == psellers[0][0].amount:
                psellers.remove(psellers[0])
                pbuyers[i][0].amount -= to_selled
                i -= 1
            else:
                psellers[0][0].amount -= to_selled
                
    def compute_all_buys(self):
        accounted_product = self.order_buyers_by_product()
        product_in_sale = self.order_sellers_by_product()
        for p in accounted_product:
            #print(f"{p} accounted product {len(accounted_product[p])}")
            self.compute_product_buy(p,product_in_sale[p],accounted_product[p])
        
    def ejecute_iteration(self, conditions : List[Condition]):
        market_products_dates = self.get_market_products_dates()
        #print("ejecute iteration")
        self.compute_all_buys()
        self.set_global_market(market_products_dates,conditions)
        self.inflation_factor = self.get_inflation_factor()
        
    def set_global_market(self,market_products_dates : List[market_Product_Dates], conditions : List[Condition]):
        compute_condition(market_products_dates,conditions)
        in_sale = []
        to_buy = [] 
        for p in market_products_dates:
            in_sale.append(Product_in_sale(p.product,normal_variation(p.price),p.external_market_offert))
            to_buy.append(AccountedProduct(p.product,p.external_market_demand))
        self.buyers = [Buyer(Global_Company(), ProductCollection(to_buy))]
        self.sellers = [Seller(Global_Company(),ProductCollection(in_sale))]

def set_global_in_sale(products : List[Product_in_sale], conditions : List[Condition]):
    in_sale = products
    for c in conditions:
        in_sale = c.get_product_in_sale(in_sale)

def buyer_sort(buyers : List[Buyer]) -> List[Buyer]:
    sorted_buyers = []
    for i in range(len(buyers)):
        total = sum([buyer.company.staff_capacity for buyer in buyers])
        capacities = [buyer.company.staff_capacity/total for buyer in buyers]
        buyer = random.choices(buyers,capacities,k=1)[0]
        sorted_buyers.append(buyer)
        buyers.remove(buyer)
    return sorted_buyers
