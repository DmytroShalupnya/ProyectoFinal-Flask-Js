import sqlite3
from requests import Session
import json
from config import API_KEY,DATA_BASE
from my_coin.utils import *
from my_coin.tools import *
from decimal import Decimal,getcontext
from datetime import datetime
from my_coin.exceptions import *
from my_coin.error_handler import *
import requests
getcontext().prec = 40

class ConexionApi(Session):
    def __init__(self, timeout: float = 20.0):
        super().__init__()
        self.BASE_URL = "https://pro-api.coinmarketcap.com"
        self.timeout = timeout
        self.headers.update({
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': API_KEY,
        })

    def get_first_100(self):
        try:
            self.params = { 
                "limit": "100",
                "convert": "EUR"
            }
            response = self.get(f"{self.BASE_URL}/v1/cryptocurrency/listings/latest", timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.Timeout:
            raise ExternalApiError("La API externa tardó demasiado en responder")
        except requests.exceptions.RequestException as e:
            raise ExternalApiError(f"Error conectando con la API externa: {str(e)}")

    def get_coin_price(self, coin_name, amount=1):
        """
        Funcion para conseguir el precio unitario de cada moneda, se debe pasar el id
        de la moneda en int.
        Devuelve el precio unitario formateado.
        """
        try:
            coin_id = get_coin_id(coin_name)
            
            self.params = {
                "id": coin_id,
                "amount": amount,
                "convert": "EUR",
            }
            response = self.get(f"{self.BASE_URL}/v2/tools/price-conversion", timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            unit_price = get_price_from_json(data)  
            return Decimal(unit_price)
        except requests.exceptions.Timeout:
            raise ExternalApiError("La API externa tardó demasiado en responder")
        except requests.exceptions.RequestException as e:
            raise ExternalApiError(f"Error conectando con la API externa: {str(e)}")
   






class ConexionBD():
    def __init__(self):
        self.db_path = DATA_BASE

    def buy_coin(self, params=[]):
        try:
            with sqlite3.connect(self.db_path) as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO movements (datetime, coin_from, amount_from, coin_to, amount_to, price_per_unit) VALUES (?,?,?,?,?,?)",
                    params
                )
                con.commit()
        except sqlite3.OperationalError as e:
            raise DatabaseError(f"Error de base de datos: {str(e)}")
        except sqlite3.IntegrityError as e:
            raise DatabaseError(f"Error de base de datos: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Error de base de datos: {str(e)}")

    def get_all_movements(self):
        try:
            with sqlite3.connect(self.db_path) as con:
                cur = con.cursor()
                cur.execute("SELECT datetime, coin_from, amount_from, coin_to, amount_to, price_per_unit FROM movements;")
                rows = cur.fetchall()
            return rows
        except sqlite3.OperationalError as e:
           raise DatabaseError(f"Error de base de datos: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Error inesperado al consultar movimientos: {str(e)}")

    def get_coin_amount(self, coin):
        try:
           
            totalAmountFrom = 0
            totalAmountTo = 0
            with sqlite3.connect(DATA_BASE) as con:
                cur = con.cursor()
                cur.execute("SELECT amount_from FROM movements WHERE coin_from = ?;", (coin,))
                amount_from = cur.fetchall()
                cur.execute("SELECT amount_to FROM movements WHERE coin_to = ?;", (coin,))
                amount_to = cur.fetchall()
            for i in amount_from:
                totalAmountFrom += Decimal(i[0])
            for i in amount_to:
                totalAmountTo += Decimal(i[0])
            amount = totalAmountTo - totalAmountFrom
            
            return amount
        except sqlite3.OperationalError as e:
            raise DatabaseError(f"Error al consultar cantidad de moneda: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al consultar cantidad: {str(e)}")

    def update_wallet(self, *coins):
        try:
            with sqlite3.connect(self.db_path, timeout=10) as con:
                cur = con.cursor()
                for coin in coins:
                    if coin.upper() == "EUR":
                        continue
                    amount = str(self.get_coin_amount(coin))
                    cur.execute(
                        """
                        INSERT INTO wallet (coin, amount)
                        VALUES (?, ?)
                        ON CONFLICT(coin) DO UPDATE SET amount = excluded.amount;
                        """,
                        (coin, amount)
                    )
                con.commit() 
        except sqlite3.OperationalError as e:
            raise DatabaseError(f"Error al actualizar wallet: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al actualizar wallet: {str(e)}")

    def get_wallet(self):
        wallet= []
        try:
            with sqlite3.connect(self.db_path) as con:
                cur = con.cursor()
                cur.execute("SELECT coin, amount FROM wallet;")
                rows = cur.fetchall()
                for i in rows:
                    if Decimal(i[1]) > 0:
                        wallet.append(i)
                return wallet
        except sqlite3.OperationalError as e:
            raise DatabaseError(f"Error al consultar wallet: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al consultar wallet: {str(e)}")

    def get_wallet_by_coin(self, coin):
        try:
            with sqlite3.connect(self.db_path) as con:
                cur = con.cursor()
                cur.execute("SELECT coin, amount FROM wallet WHERE coin = ?;", (coin,))
                coin_amount = cur.fetchone()
                return coin_amount
        except sqlite3.OperationalError as e:
            raise DatabaseError(f"Error al consultar moneda en wallet: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado: {str(e)}")

    def on_start_wallet_update(self):
        coins = []
        try:
            with sqlite3.connect(self.db_path) as con:
                cur = con.cursor()
                cur.execute("SELECT coin_from, coin_to from movements;")
                result = cur.fetchall()
                for par in result:
                    for item in par:
                        if item not in coins:
                            coins.append(item)
                for i in coins:
                    self.update_wallet(i)        
                
        except Exception as e:
            return e    






class Status():
    def __init__(self):
        self.api = ConexionApi()
        self.dataBase = ConexionBD()

    def invested(self):
        invested = 0
        try:
            with sqlite3.connect(self.dataBase.db_path) as con:
                cur = con.cursor()
                cur.execute("SELECT amount_from FROM movements where coin_from = 'EUR';")
                movements = cur.fetchall()
                for i in movements:
                    invested += Decimal(i[0])
                if invested == None:
                    invested = 0
                
            return str(invested)
        except sqlite3.OperationalError as e:
            raise TransactionError(f"Error al calcular inversión: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al calcular inversión: {str(e)}")
        
    def recovered(self):
        recoveredTotal = 0
        try:
            with sqlite3.connect(self.dataBase.db_path) as con:
                cur = con.cursor()
                cur.execute("SELECT amount_to FROM movements where coin_to = 'EUR';")
                recovered = cur.fetchall()
                for i in recovered:
                    recoveredTotal += Decimal(i[0])
                if recovered == None:
                    recoveredTotal = 0
               
            return str(recoveredTotal)
        except sqlite3.OperationalError as e:
            raise TransactionError(f"Error al calcular recuperado: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al calcular recuperado: {str(e)}")
    
    def valor_compra(self):
        try:
            invertido = Decimal(self.invested())
            recuperado = Decimal(self.recovered())
            value = invertido - recuperado
            if value < 0:
                value = 0
            return value
        except Exception as e:
            raise Exception(f"Error al calcular valor de compra: {str(e)}")
    
    def current_wallet_value(self):
        try:
            total_wallet_value = Decimal()
            wallet_list = self.dataBase.get_wallet()
            
            for i in wallet_list:
                if Decimal(i[1]) > 0:
                    total_wallet_value += self.api.get_coin_price(i[0], i[1])
                else:
                    continue
            return str(total_wallet_value)
        except Exception as e:
            raise Exception(f"Error al calcular valor total del wallet: {str(e)}")

    def diference(self):
        
        wallet = Decimal(self.current_wallet_value())
        valor_compra = Decimal(self.valor_compra())
        if valor_compra/wallet > 0.999999 and valor_compra/wallet < 1:
            diference = 0
            return diference
        try:
            diference = ((wallet - valor_compra) / valor_compra) * 100
        except Exception:
            diference = 0
        return str(diference)
    





def amount_coin_exchange(coin_from, coin_to, amount_from):
    try:
        api = ConexionApi()
        bd = ConexionBD()
        units_to_buy = 0.0
        amount_from_mod = amount_from.replace(",","")
        amount_from_dec = Decimal(amount_from_mod)

        if coin_from == "EUR":
            coin_from_price = amount_from_dec    
            coin_to_price = api.get_coin_price(coin_to)
            units_to_buy = coin_from_price / coin_to_price
        
        elif coin_to == "EUR" and wallet_check(amount_from_dec, bd.get_coin_amount(coin_from)):
            units_to_buy = Decimal(api.get_coin_price(coin_from, amount_from_dec)) 
        
        else:
            if wallet_check(amount_from_dec, bd.get_coin_amount(coin_from)) == True:
                coin_from_price = Decimal(api.get_coin_price(coin_from, amount=amount_from))
                coin_to_price = Decimal(api.get_coin_price(coin_to))
                units_to_buy = coin_from_price / coin_to_price
            else:
                units_to_buy = f"Cantidad a vender ({amount_from} {coin_from}), mayor que la disponible ({bd.get_coin_amount(coin_from)} {coin_from})"
                return units_to_buy
        return str(round(units_to_buy,7))
    except Exception as e:
        raise Exception(f"Error al calcular intercambio: {str(e)}")







class Transaction():
    def __init__(self, json_list):
        try:
            self.api = ConexionApi()
            self.bd = ConexionBD()
            self.datos = json_list
            self.moneda_from = self.datos["moneda_from"]
            self.moneda_to = self.datos["moneda_to"]
            self.amount_to = str(self.datos["amount_to"])
            self.pu = 0
            self.amount_from = str(self.datos["amount_from"])
            self.time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if self.moneda_from == "EUR":
                self.buy_crypto()
            elif self.moneda_to == "EUR":
                self.sell_crypto()
            else:
                self.trading()
        except KeyError as e:
            raise TransactionError(f"Datos incompletos en la transacción: {str(e)}")
        except Exception as e:
            raise TransactionError(f"Error al procesar transacción: {str(e)}")
    
    def sell_crypto(self):
        try:
            self.pu = Decimal(self.api.get_coin_price(self.moneda_from))
            self.bd.buy_coin([self.time_now, self.moneda_from,  self.amount_from, 
                             self.moneda_to, self.amount_to, str(round(self.pu, 4))])
            self.bd.update_wallet(self.moneda_from, self.moneda_to)
        except Exception as e:
            raise TransactionError(f"Error al vender crypto: {str(e)}")
    
    def buy_crypto(self):
        try:
            self.pu = Decimal(self.api.get_coin_price(self.moneda_to))
            self.bd.buy_coin([self.time_now, self.moneda_from, self.amount_from, 
                             self.moneda_to, self.amount_to, str(round(self.pu, 4))])
            self.bd.update_wallet(self.moneda_to, self.moneda_from)
        except Exception as e:
            raise TransactionError(f"Error al comprar crypto: {str(e)}")
       
    def trading(self):
        try:
            self.pu = self.api.get_coin_price(self.moneda_to)
            self.bd.buy_coin([self.time_now, self.moneda_from,  self.amount_from, 
                             self.moneda_to, self.amount_to, str(round(self.pu, 4))])
            self.bd.update_wallet(self.moneda_to,self.moneda_from)
            
        except Exception as e:
            raise TransactionError(f"Error en el movimiento de trading: {str(e)}")
        