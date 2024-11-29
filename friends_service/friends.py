from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
from datetime import datetime
from CustomerAccessor.CustomerAccessor import CustomerAccessor as friend_CA
from jsonable import Jsonable

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/accounts/friends/hello_world', methods=['POST'])
def hello_world():
    return jsonify(Jsonable(data="Hello, World!"))

@app.route('/accounts/<int:account_id>/friends', methods=['GET'])
def friends(account_id):
    ca = friend_CA()
    ca.login(account_id)
    friends = list()

    friendships = ca.get_friendships()
    if friendships:
        for friendship in friendships:
            if friendship.account1 != str(account_id):
                friend = friendship.account1
            else:
                friend = friendship.account2
            friends.append(friend)
    return jsonify(Jsonable(friends=friends))


@app.route('/accounts/<int:account_id>/friends/requests/sent', methods=['GET'])
def get_sent_requests(account_id):
    ca = friend_CA()
    ca.login(account_id)

    requests = ca.get_sent_requests()
    if type(requests) == list:
        return jsonify(Jsonable(friends=[request.target for request in requests]))
    return jsonify(Jsonable(function="get_sent_requests", 
                            error="Unable to get sent requests"))

@app.route('/accounts/<int:account_id>/friends/requests/received', methods=['GET'])
def get_received_requests(account_id):
    ca = friend_CA()
    ca.login(account_id)

    requests = ca.get_received_requests()
    if type(requests) == list:
        return jsonify(Jsonable(friends=[request.target for request in requests]))
    return jsonify(Jsonable(function="get_received_requests", 
                            error="Unable to get received requests"))


@app.route('/accounts/<int:account_id>/friends/requests/send', methods=['POST'])
def send_request(account_id, friend_id):
    return jsonify(Jsonable("Successfully called send_request"))
    ca = friend_CA()
    ca.login(account_id)

    result = ca.send_friend_request(friend_id)
    return jsonify(Jsonable(function="send_request", 
                            success=bool(result)))

@app.route('/accounts/<int:account_id>/friends/requests/accept', methods=['POST'])
def accept_request(account_id, friend_id):
    ca = friend_CA()
    ca.login(account_id)

    request = ca.get_received_request( friend_id )
    if not request: return False
    result = ca.accept_request( request )

    return jsonify(Jsonable(function="accept_request", 
                            success=bool(result)))

@app.route('/accounts/<int:account_id>/friends/requests/reject', methods=['POST'])
def reject_request(account_id, friend_id):
    ca = friend_CA()
    ca.login(account_id)

    request = ca.get_received_request( friend_id )
    if not request: return False
    result = ca.reject_request( request )

    return jsonify(Jsonable(function="reject_request", 
                            success=bool(result)))


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5003, debug=True)


