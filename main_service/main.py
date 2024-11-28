from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

MAIN_SERVICE_URL = 'http://main-service:5001/accounts'
SECURITY_SERVICE_URL = 'http://security-service:5002/accounts'



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/accounts/create')
def load_create_account():
    return render_template('account_create.html')

@app.route('/accounts/login')
def load_login_account():
    return render_template('account_login.html')

@app.route('/accounts/create_account/post', methods=['POST'])
def add_account():
    account_data = {
        'username': request.form['username'],
        'password': request.form['password']
    }

    try:
        response = requests.post(SECURITY_SERVICE_URL+'/create_account/post', json=account_data)
        response.raise_for_status()
        flash('Account added successfully!')

    except requests.RequestException as e:
        flash(f'Error adding account: {str(e)}')
        return jsonify({"error":str(e)})

    json_result = response.json()
    return json_result

    return redirect(url_for('index'))

@app.route('/accounts/login/get', methods=['POST'])
def account_login():
    account_data = {
        'username': request.form['username'],
        'password': request.form['password']
    }

    try:
        response = requests.get(SECURITY_SERVICE_URL+'/login/get', json=account_data)
        response.raise_for_status()
        flash('Account added successfully!')

    except requests.RequestException as e:
        flash(f'Error adding account: {str(e)}')
        return jsonify({ "error":str(e)})

    json_result = response.json()
    return json_result




if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001, debug=True)


