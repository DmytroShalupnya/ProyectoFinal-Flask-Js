from my_coin.conection import ConexionBD
from my_coin.utils import *
from my_coin.tools import wallet_check
from decimal import Decimal



class PurchaseDataController():
    def __init__(self, data):
        self.coin_from = data["moneda_from"]
        self.amount_from = data["amount_from"]
        self.coin_to = data['moneda_to']
        self.amount_to = data["amount_to"]
        self.db = ConexionBD()
        self.dataOk = self.amounts_control() and self.coins_controll()
         
    
    def amounts_control(self):
        try:
            if self.coin_from != "EUR":
                if wallet_check(Decimal(self.amount_from), self.db.get_coin_amount(self.coin_from)):
                    try:
                        return float(self.amount_from) > 0 and float(self.amount_to) > 0
                    except ValueError:
                        return False    
                else:
                    return False
            else:
                return float(self.amount_to) > 0 and Decimal(self.amount_from) > 0 
        except Exception:
            return False 
        
            

    def coins_controll(self):
        try:
            result = 0
            if self.coin_from != self.coin_to:
                for coin in self.coin_from, self.coin_to:
                    if coin != "EUR":
                        result += coin.lower() in COIN_ID
                    else:
                        result += 1
            if result == 2:
                return True            
            else:
                return False   
        except Exception:
            return False    