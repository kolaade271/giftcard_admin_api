# app.py
from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps
from Class.admin import Admin
import os
from marshmallow import ValidationError
from flask_cors import CORS
from Class.validation import admin_login_schema, admin_rate_schema, admin_sell_trx_schema
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_KEY') 
CORS(app)
admin = Admin()  # Initialize the Admin class
jwt_config =  app.config["SECRET_KEY"]

# Helper function to require JWT token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'status':False,'message': 'Token is missing!'}), 403
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/pw', methods=['POST'])
def pw():
    auth = request.get_json()
    pw = auth["password"]
    res = admin.generate_sha512(pw)
    return jsonify({"pw":res})

# Route for user login to generate a JWT
@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()
    try:
        validated_data = admin_login_schema.load(auth)
        res = admin.get_admin(auth,jwt_config)
        if res:
            return jsonify(res)
        return jsonify({'message': 'Invalid credentials!'}), 401
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400


@app.route('/sell', methods=['GET'])
@token_required
def get_sell(hello):
    user_data = admin.sell()
    if user_data:
        return jsonify(user_data)
    return jsonify({'status':False,'message': 'Transaction not found'}), 404

@app.route('/buy', methods=['GET'])
@token_required
def get_buy(hello):
    user_data = admin.buy()
    if user_data:
        return jsonify(user_data)
    return jsonify({'status':False,'message': 'Transaction not found'}), 404


@app.route('/transactions', methods=['GET'])
@token_required
def get_transactions(hello):
    user_data = admin.transactions()
    if user_data:
        return jsonify(user_data)
    return jsonify({'status':False,'message': 'Transaction not found'}), 404


@app.route('/pending_sell_transactions', methods=['GET'])
@token_required
def get_sell_pedning_transactions(hello):
    user_data = admin.pending_transaction()
    if user_data:
        return jsonify(user_data)
    return jsonify({'status':False,'message': 'Transaction not found'}), 404

@app.route('/update_sell_rate', methods=['POST'])
@token_required
def update_sell(hello):
    data = request.get_json()
    print(data)
    try:
        admin_rate_schema.load(data)
        user_data = admin.update_sell_rate(data)
        if user_data:
            return jsonify(user_data)
        return jsonify({'status':False,'message': 'Transaction not found'}), 404
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400


@app.route('/update_buy_rate', methods=['POST'])
@token_required
def update_buy(hello):
    data = request.get_json()
    try:
        validated_data = admin_rate_schema.load(data)
        user_data = admin.update_buy_rate(data)
        if user_data:
            return jsonify(user_data)
        return jsonify({'status':False,'message': 'Transaction not found'}), 404
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    

@app.route('/update_sell_transaction', methods=['POST'])
@token_required
def update_sell_transactiom(hello):
    data = request.get_json()
    try:
        validated_data = admin_sell_trx_schema.load(data)
        user_data = admin.transaction_sell_update(data)
        if user_data:
            return jsonify(user_data)
        return jsonify({'status':False,'message': 'Transaction not found'}), 404
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9200, debug=True)
