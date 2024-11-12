from Friends.DAO.Friend import FriendRequest, Friendship, Account

class CustomerAccessor:
    def __init__( self ):
        self.account = None

    ##### login #####
    def login( self, account_id ):
        self.account = Account(account_id)

    ##### friend request #####
    def get_sent_requests( self ):
        if self.account:
            return self.account.get_sent_requests()
        return False

    def get_received_requests( self ):
        if self.account:
            return self.account.get_received_requests()
        return False

    ##### friend request actions #####
    def send_friend_request( self, friend_id ):
        if self.account:
            return FriendRequest(self.account.id, friend_id).create()
        return False

    def accept_request( self, request ):
        if self.account and request.target == self.account.id:
            friendship = Friendship(request.requester,request.target)
            if friendship.create():
                return request.remove()
        return False

    def reject_request( self, request ):
        if self.account and request.target == self.account.id:
            return request.remove()
        return False


    ##### friendships #####
    def get_friendships( self ):
        if self.account:
            return self.account.get_friendships()
        return False

    def get_friendship( self, friend_id ):
        if self.account:
            return self.account.get_friendship(friend_id)
        return False

    def remove_friendship( self, friendship ):
        # verify account is one of the accounts in the friendship
        if self.account and \
                   (friendship.account1 == self.account.id \
                    or friendship.account2 == self.account.id):
            return friendship.remove()
        return False




