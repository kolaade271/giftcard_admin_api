from pymongo import MongoClient , DESCENDING
import json
import random
from bson.objectid import ObjectId
from datetime import datetime, timezone
import os
class Database:
    def __init__(self):
       
        self.client = MongoClient(os.getenv('DATABASE_URL') )
        self.db = self.client['Giftcard_Db']
        
    def admin_login(self,data):
        self.buy = self.db['admin_login']
        result = self.buy.find_one(data) 
        if result:
            if "_id" in result:
                result["_id"] = str(result["_id"])
            return result
        else:
            return None
        
    
    def admin_login(self,data):
        self.admin = self.db['admin_login']
        result = self.admin.find_one(data) 
        if result:
            if "_id" in result:
                result["_id"] = str(result["_id"])
            return result
        else:
            return None
        
    
    def get_all_transactions(self):
        self.transactions = self.db["transactions"]
        transactions = self.transactions.find().sort("createdAt", DESCENDING)

        transactions_list = [
        {**transaction, "_id": str(transaction["_id"])} 
        for transaction in transactions
         ]
        return transactions_list
    
    def get_all_sell_transactions(self):
        self.transactions = self.db["transactions"]
        transactions = self.transactions.find({"status":"pending", "transaction_type":"sell"}).sort("createdAt", DESCENDING)

        transactions_list = [
        {**transaction, "_id": str(transaction["_id"])} 
        for transaction in transactions
        ]
        return transactions_list
    
    
    def get_all_sell(self):
        self.transactions = self.db["sell_card"]
        transactions = self.transactions.find()

        transactions_list = [
        {**transaction, "_id": str(transaction["_id"])} 
        for transaction in transactions
        ]
        return transactions_list
    
    
    
    def get_all_buy(self):
        self.transactions = self.db["buy_card"]
        transactions = self.transactions.find()

        transactions_list = [
        {**transaction, "_id": str(transaction["_id"])} 
        for transaction in transactions
        ]
        return transactions_list
    
    


    def update_rate(self,_id, rate,table):
        self.trx = self.db[table]
        if isinstance(_id, str):
            _id = ObjectId(_id)
        result = self.trx.update_one(
            {'_id': _id},  
            {'$set': {'rate': rate}}  
        )
        if result.matched_count > 0:
            return True
        return False
    
    
    def update_tansactions(self,_id, status,table):
        self.trx = self.db[table]
        if isinstance(_id, str):
            _id = ObjectId(_id)
        result = self.trx.update_one(
            {'_id': _id},  
            {'$set': {'status': status}}  
        )
        if result.matched_count > 0:
            return True
        return False
        
        
    def fetch_transaction(self,_id):
        self.trx = self.db['transactions']
        if isinstance(_id, str):
            _id = ObjectId(_id)
        result = self.trx.find_one({"_id":_id})
        if result:
            if "_id" in result:
                result["_id"] = str(result["_id"])
            return result
        else:
            return None
        