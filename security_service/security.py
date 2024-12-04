from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
from datetime import datetime
from CustomerAccessor.CustomerAccessor import CustomerAccessor as security_CA
from jsonable import Jsonable

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/accounts/create_account/post', methods=['POST'])
def add_account():
    if not request.json:
        return jsonify({'error': 'No data provided'}), 400

    required_fields = ['username', 'password']
    if not all(field in request.json for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    username = request.json['username']
    password = request.json['password']

    ca = security_CA()
    result = ca.create_account(username, password)
    
    if not result:
        return Jsonable(error="Unable to add account")

    return jsonify(Jsonable(function="add_account", success=1, 
                            username=username, password=password 
                            ))

@app.route('/accounts/login/get', methods=['GET'])
def account_login():
    if not request.json:
        return jsonify({'error': 'No data provided'}), 400

    required_fields = ['username', 'password']
    if not all(field in request.json for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    username = request.json['username']
    password = request.json['password']

    ca = security_CA()
    result = ca.login(username, password)
    if not result:
        return jsonify(Jsonable(error="Unable to login",success=0))

    userid = ca.get_userid()
    if not userid:
       return jsonify(Jsonable(error="Unable to get user id"))

    return jsonify(Jsonable(function="account_login", username=username, 
                            password=password, userid=userid, 
                            success=1))


@app.route('/accounts/<int:account_id>/username/get')
def get_username(account_id):
    ca = security_CA()
    return jsonify(Jsonable(ca.get_friend_username(account_id)))



if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5002, debug=True)


