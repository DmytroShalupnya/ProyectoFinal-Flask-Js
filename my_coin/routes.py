from . import app
from flask import redirect, render_template, request, jsonify
from my_coin.conection import *
from my_coin.error_handler import *
from datetime import datetime
from my_coin import app
from my_coin.tools import *
from my_coin.utils import *
from my_coin.controller import PurchaseDataController
ahora = datetime.now()
t_now = ahora.strftime("%Y-%m-%d %H:%M:%S:%MS")



@app.route("/")
def index(): 
    
    bd=ConexionBD()
    api = ConexionApi()
    datos =api.get_first_100()
    get_coin_ids(datos, COIN_ID)
    bd.on_start_wallet_update()
    my_coins = bd.get_wallet()
    return render_template("index.html", myCoins= walletFormat(my_coins) , aviableCoins = get_aviable_coins(COIN_ID))
    


@app.route("/api/v1/tasa/<moneda_from>/<moneda_to>", methods=["GET"])
def exchange_rate(moneda_from, moneda_to):
    status = "succes"
    try:
        amount_from = request.args.get("amount")
        amount_aviable_to_purchase = amount_coin_exchange(moneda_from, moneda_to, amount_from)
        try: 
            float(amount_aviable_to_purchase)
        except Exception:    
            status = "Not Completed"
        finally:
            return jsonify({
            "purchasedAmount": amount_aviable_to_purchase,
            "status":status,
            }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    


@app.route("/api/v1/movimientos", methods =["GET"])
def all_movements():
    try:
        bd=ConexionBD()
        all_movements = bd.get_all_movements()
        return jsonify({
            "datos": all_movements,
            "status": "Ok"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

    

@app.route("/api/v1/compra", methods=["POST"])
def buy_coin():
    
    try:
        datos = request.json
        controller = PurchaseDataController(datos)
       
        if controller.dataOk:
            transaction = Transaction(datos)
            return jsonify({
            "message":"Purchase Done!",
            "status":"ok"
            })
        else:
            return jsonify({
                "message":"Purchase cancelled. Incorrect purchase data",
                "status": "error"
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 400
       
    

@app.route("/api/v1/status")
def show_status():
    try:
        status = Status()
        invested = f"{status.invested()}"
        recovered = f"{status.recovered()}"
        valor_compra = f"{status.valor_compra()}"
        wallet_value= f"{status.current_wallet_value()}"
        diference = status.diference()
        return jsonify({
            "invested":invested,
            "recovered":recovered,
            "valorCompra":valor_compra,
            "wallet":wallet_value,
            "diference":diference,
            "status": "OK"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/prueba")
def prueba():
    db = ConexionBD()
    answer = db.onStartWalletUpdate()

    return jsonify({
        "answer":answer

    })   

    
    
  

