from Friends.CustomerAccessor.CustomerAccessor import CustomerAccessor as friend_CA
from Security.CustomerAccessor.CustomerAccessor import CustomerAccessor as security_CA


# /
def index():
    pass

# /accounts
def accounts():
    pass

# /accounts/create
def account_create(username, password):
    ca = security_CA()
    result = ca.create_account(username, password)
    return result

# /accounts/login
def account_login(username, password):
    ca = security_CA()
    result = ca.login(username, password)
    if not result: return False
    return ca.get_userid()

# /accounts/<account#>/friends
def get_friends(account_id):
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
    return friends

# /accounts/<account#>/friends/requests/sent
def get_sent_requests(account_id):
    ca = friend_CA()
    ca.login(account_id)

    requests = ca.get_sent_requests()
    if requests:
        return [request.target for request in requests]
    return list()

# /accounts/<account#>/friends/requests/received
def get_received_requests(account_id):
    ca = friend_CA()
    ca.login(account_id)

    requests = ca.get_received_requests()
    if requests:
        return [request.requester for request in requests]
    return list()

# /accounts/<account#>/friends/requests/sent/<friend#>
def get_sent_request(account_id, friend_id):
    ca = friend_CA()
    ca.login(account_id)

    sent_request = ca.get_sent_request( friend_id )
    return sent_request

# /accounts/<account#>/friends/requests/sent/send/<friend#>
def send_request(account_id, friend_id):
    ca = friend_CA()
    ca.login(account_id)

    return ca.send_friend_request(friend_id)

# /accounts/<account#>/friends/requests/received/<friend#>
def get_received_request(account_id, friend_id):
    ca = friend_CA()
    ca.login(account_id)

    sent_request = ca.get_received_request( friend_id )
    return sent_request

# /accounts/<account#>/friends/requests/received/<friend#>/accept
def accept_request(account_id, friend_id):
     ca = friend_CA()
     ca.login(account_id)

     request = ca.get_received_request( friend_id )
     if not request: return False
     return ca.accept_request( request )

# /accounts/<account#>/friends/requests/received/<friend#>/reject
def reject_request(account_id, friend_id):
     ca = friend_CA()
     ca.login(account_id)

     request = ca.get_received_request( friend_id )
     if not request: return False
     return ca.reject_request( request )

# /accounts/<account#>/items/<itemname>

# /accounts/<account#>/items/<itemname>/remove

# /accounts/<account#>/items/<itemname>/add


# for testing
def view_requests():
    sent1 = get_sent_requests(userid)
    sent2 = get_sent_requests(userid2)
    received1 = get_received_requests(userid)
    received2 = get_received_requests(userid2)
    print( f"{sent1}\n{sent2}\n{received1}\n{received2}\n\n" )
def view_friends():
    friends1 = get_friends(userid)
    print(friends1)
    friends2 = get_friends(userid2)
    print(friends2)
    print()
    
if __name__ == "__main__":
    import pdb

    # step 1: login
    username = "me monolithic"
    password = "password"
    account_create(username, password)
    userid = account_login(username, password)
    assert bool(userid) == True

    username2 = "me mon2"
    password2 = "password2"
    account_create(username2, password2)
    userid2 = account_login(username2, password2)
    assert bool(userid2) == True

    # 2.0: view friends
    view_friends()


    # 2.1: view requests
    view_requests()


    # 2.2: send request
    print(send_request(userid, userid2))


    # 2.3: access request
    view_requests()
    print(get_sent_request(userid,userid2))
    print(get_sent_request(userid2,userid))
    print(get_sent_request(userid,userid))
    print(get_sent_request(userid2,userid2))
    print()

    print(get_received_request(userid,userid2))
    print(get_received_request(userid2,userid))
    print(get_received_request(userid,userid))
    print(get_received_request(userid2,userid2))
    print()


    # 2.4: reject request
    assert reject_request(userid,userid) == False
    assert reject_request(userid2,userid2) == False
    reject_request(userid2,userid)
    view_requests()


    # 2.5 accept request
    print(send_request(userid,userid2))
    assert accept_request(userid,userid2) == False
    print(accept_request(userid2,userid))
    view_requests()
    view_friends()

    pdb.set_trace()











