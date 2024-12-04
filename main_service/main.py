from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
from datetime import datetime
from jsonable import Jsonable


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

MAIN_SERVICE_URL = 'http://main-service:5001'
SECURITY_SERVICE_URL = 'http://security-service:5002/accounts'
FRIENDS_SERVICE_URL = 'http://friends-service:5003/accounts' # need to append account#
ITEM_SERVICE_URL = 'http://item-service:5004/accounts'


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

    if int(json_result["success"]):
        userid = int(json_result["userid"])
        return redirect(url_for('load_account', account_id=userid))

    return redirect(url_for('load_create_account'))





@app.route('/accounts/<int:account_id>')
def load_account(account_id):
    return render_template('account.html', account_id=account_id)


@app.route('/accounts/<int:account_id>/friends')
def friends(account_id):
    # get friends
    try:
        response = requests.get(FRIENDS_SERVICE_URL+f'/{account_id}/friends' )
        response.raise_for_status()
        flash('Account added successfully!')

    except requests.RequestException as e:
        flash(f'Error adding account: {str(e)}')
        return jsonify({ "error":str(e)})

    friends = response.json()["friends"]

    # get received requests
    try:
        response = requests.get(FRIENDS_SERVICE_URL+f'/{account_id}/friends/requests/sent' )
        response.raise_for_status()
        flash('Account added successfully!')

    except requests.RequestException as e:
        flash(f'Error adding account: {str(e)}')
        return jsonify({ "error":str(e)})

    sent_requests = response.json()["friends"]

    # get received requests
    try:
        response = requests.get(FRIENDS_SERVICE_URL+f'/{account_id}/friends/requests/received' )
        response.raise_for_status()
        flash('Account added successfully!')

    except requests.RequestException as e:
        flash(f'Error adding account: {str(e)}')
        return jsonify({ "error":str(e)})

    received_requests = response.json()["friends"]


    return render_template('friends.html', 
                           account_id=account_id, 
                           friends=friends, 
                           sent_requests = sent_requests, 
                           received_requests = received_requests)

@app.route('/accounts/<int:account_id>/friends/requests/sent', methods=['GET'])
def get_sent_requests(account_id):
    result = requests.get(FRIENDS_SERVICE_URL
                           + f'/{account_id}'
                           + '/friends/requests/sent', 
                          account_id=account_id)
    return result

@app.route('/accounts/<int:account_id>/friends/requests/received', methods=['GET'])
def get_received_requests(account_id):
    result = requests.get(FRIENDS_SERVICE_URL
                           + f'/{account_id}'
                           + '/friends/requests/received', 
                          account_id=account_id)
    return result


@app.route('/accounts/<int:account_id>/friends/requests/send', methods=['POST'])
def send_request(account_id):
    friend_id = request.form["friend_id"]

    my_json = jsonify(Jsonable(account_id=account_id, friend_id=friend_id)).json

    try:
        link = f'{FRIENDS_SERVICE_URL}/{account_id}/friends/requests/send'
        response = requests.post(link, json=my_json)
        response.raise_for_status()
        flash('Success!')

    except requests.RequestException as e:
        flash(f'Error adding account: {str(e)}')
        return jsonify(Jsonable( function="send_request", 
                                 error=str(e)))

    result = response.json()

    return friends(account_id)


@app.route('/accounts/<int:account_id>/friends/requests/accept', methods=['POST'])
def accept_request(account_id):
    friend_id = request.form["friend_id"]

    my_json = jsonify(Jsonable(account_id=account_id, friend_id=friend_id)).json

    try:
        link = f'{FRIENDS_SERVICE_URL}/{account_id}/friends/requests/accept'
        response = requests.post(link, json=my_json)
        response.raise_for_status()
        flash('Success!')

    except requests.RequestException as e:
        flash(f'Error adding account: {str(e)}')
        return jsonify(Jsonable( function="accept_request", 
                                 error=str(e)))

    result = response.json()

    return friends(account_id)


@app.route('/accounts/<int:account_id>/friends/requests/reject', methods=['POST'])
def reject_request(account_id):
    friend_id = request.form["friend_id"]

    my_json = jsonify(Jsonable(account_id=account_id, friend_id=friend_id)).json

    try:
        link = f'{FRIENDS_SERVICE_URL}/{account_id}/friends/requests/reject'
        response = requests.post(link, json=my_json)
        response.raise_for_status()
        flash('Success!')

    except requests.RequestException as e:
        flash(f'Error adding account: {str(e)}')
        return jsonify(Jsonable( function="reject_request", 
                                 error=str(e)))

    result = response.json()

    return friends(account_id)




@app.route('/accounts/<int:account_id>/items')
def items(account_id):
    link = f'{SECURITY_SERVICE_URL}/{account_id}/username/get'
    response = requests.get(link)
    username = eval(response.json()['other'])[0]

    link = f'{ITEM_SERVICE_URL}/{username}/items'
    response = requests.get(link, timeout=10)
    my_items = response.json()

    return render_template('items.html', account_id=account_id, items=my_items, friend=False)


@app.route('/accounts/<int:account_id>/friends/access', methods=['POST'])
def access_friend(account_id):
    friend_id = request.form["friend_id"]

    link = f'{SECURITY_SERVICE_URL}/{friend_id}/username/get'
    response = requests.get(link)
    username = eval(response.json()['other'])[0]

    link = f'{ITEM_SERVICE_URL}/{username}/items'
    response = requests.get(link, timeout=10)
    my_items = response.json()

    return render_template('items.html', account_id=friend_id, items = my_items, friend=True)

@app.route('/accounts/<int:account_id>/items/add', methods=['GET','POST'])
def add_item(account_id):
    link = f'{SECURITY_SERVICE_URL}/{account_id}/username/get'
    response = requests.get(link)
    username = eval(response.json()['other'])[0]

    if request.method == 'POST':
        name = str(request.form.get('name'))
        source = str(request.form.get('source'))

    my_json = jsonify(Jsonable(name=name,source=source)).json

    link = f'{ITEM_SERVICE_URL}/{username}/items/add/{name}/{source}'
    response = requests.post(link, json=my_json)

    return redirect(url_for('items', account_id=account_id))


@app.route('/accounts/<int:account_id>/items/remove', methods=['GET','POST'])
def remove_item(account_id):
    link = f'{SECURITY_SERVICE_URL}/{account_id}/username/get'
    response = requests.get(link)
    username = eval(response.json()['other'])[0]

    if request.method == 'POST':
        name = str(request.form.get('removeName'))
        source = str(request.form.get('removeSource'))

    my_json = jsonify(Jsonable(name=name,source=source)).json

    link = f'{ITEM_SERVICE_URL}/{username}/items/remove/{name}/{source}'
    response = requests.post(link, json=my_json)

    return redirect(url_for('items', account_id=account_id))



if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001, debug=True)


