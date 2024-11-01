from flask import jsonify
import json
import requests
from Class.database import Database
import jwt
import datetime
import hashlib


class Admin:
    def __init__(self):
        self.database = Database()
        
    
    def send(self,payload):
        headers = {
            "Content-Type": "application/json"
                   }
        response = requests.post("http://127.0.0.1:5000/notification", headers=headers, data=json.dumps(payload))
        return response

        
        
    def generate_sha512(self,input_text):
        sha512_hash = hashlib.sha512(input_text.encode()).hexdigest()
        return sha512_hash
       

    def get_admin(self, data, jwt_sec):
        password = self.generate_sha512(data["password"])
        check_data = {
            "username":data["username"],
            "password": password
        }
        data = self.database.admin_login(check_data)
        if data:
            token = jwt.encode({
                'name': data["full_name"],
                'username': data["username"],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=100010080)
            }, jwt_sec, algorithm="HS256")
            return {'status':True,'token': token}
        return False
        
    
    def transactions(self):
        trx = self.database.get_all_transactions()
        if trx:
            return {
                "status":True,
                "data":trx
            }
        return False
    
    def pending_transaction(self):
        trx = self.database.get_all_sell_transactions()
        if trx:
            return {
                "status":True,
                "data":trx
            }
        return False
    
    
    def sell(self):
        trx = self.database.get_all_sell()
        if trx:
            return {
                "status":True,
                "data":trx
            }
        return False
    
    def buy(self):
        trx = self.database.get_all_buy()
        if trx:
            return {
                "status":True,
                "data":trx
            }
        return False
    
    
    def update_sell_rate(self,data):
        _id = data["_id"]
        rate = data["rate"]
        table = "sell_card"
        trx = self.database.update_rate(_id,rate,table)
        if trx:
            return {
                "status":True,
                "data":trx
            }
        return False
    
    def update_buy_rate(self,data):
        _id = data["_id"]
        rate = data["rate"]
        table = "buy_card"
        trx = self.database.update_rate(_id,rate,table)
        if trx:
            return {
                "status":True,
                "data":trx
            }
        return False
    
    def transaction_sell_update(self,data):
        _id = data["_id"]
        status = data["status"]
        table = "transactions"
        get_trx = self.database.fetch_transaction(_id)
        if get_trx and get_trx["status"] =="pending":
            trx = self.database.update_tansactions(_id,status,table)
            order_id = get_trx["order_id"]
            message = f"We cannot process your transaction with Reference ID: {order_id},"
            if status == "completed":
                message = f"*Good news !!!*\nYour payment has been processed and you should receive it within 5-10 minutes.\n\nReference ID: {order_id}"
            if trx:
                send={"status": "success", "message": message, "phone": get_trx["user_id"]}
                self.send(send)
                return {
                    "status":True,
                    "data":trx
                }
            return False
        return False
    

