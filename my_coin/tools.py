from my_coin.utils import *




def get_coin_id(coinName):
    for name, id in COIN_ID.items():
        if name == coinName.lower():
            return id
   
def get_aviable_coins(incoming_dict):
    
    aviable_coins = []
    for name, id in incoming_dict.items():
        aviable_coins.append(name.capitalize())

    return aviable_coins    

def get_all_movements():
    pass    

def get_price_from_json(lista):
    price = lista["data"]["quote"]["EUR"]["price"]
    return price
 

def get_coin_ids(incoming_dic, new_dict):
    
    for i in incoming_dic["data"]:
        new_dict[i["name"].lower()]= i["id"] 



def wallet_check(incoming_amount, wallet_amount):
    if incoming_amount > wallet_amount:
        return False
    else:
        return True

def json_cleaner(json):
    json_clean = []
    for i in json["data"]:
        
        json_clean.append({
            "name": i["name"],
            "symbol": i["symbol"],
            "pu_EUR":i["quote"]["EUR"]["price"],
            "timestamp": json["status"]["timestamp"]
        })
    
    return json_clean

def walletFormat(wallet_list):
    walletListForm = []
    for coin, amount in wallet_list: 
        if '.' in amount:
            parte_entera, parte_decimal = amount.split('.')
        else:
            parte_entera = amount
            parte_decimal = ''
        parte_entera_formateada = ''
        for i, digito in enumerate(reversed(parte_entera)):
            if i > 0 and i % 3 == 0:
                parte_entera_formateada = ',' + parte_entera_formateada
            parte_entera_formateada = digito + parte_entera_formateada
        if parte_decimal:
            walletListForm.append([coin, parte_entera_formateada + '.' + parte_decimal]) 
        else:
            walletListForm.append([coin, parte_entera_formateada]) 
    
    return walletListForm
   
             
                

