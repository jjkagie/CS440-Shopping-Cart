from Friends.DAO.DAO import DAO
from Friends.DatabaseAccessor.DatabaseAccessor import database_accessor
import pdb


class Friendship(DAO):
    def __init__( self, account1, account2 ):
        self.account1 = str(account1)
        self.account2 = str(account2)

    def load( self ):
        result = database_accessor.run_select("SELECT * FROM Friendship WHERE " + \
                                            "account1=%s AND account2=%s",
                                            self.account1, self.account2)
        return bool(result)

    def create( self ):
        return database_accessor.run_change("INSERT INTO Friendship VALUES (%s,%s)",
                                            self.account1, self.account2)

    def remove( self ):
        return database_accessor.run_change("DELETE FROM Friendship WHERE " + \
                                            "account1=%s AND account2=%s",
                                            self.account1, self.account2)

    def update( self ):
        return False


class FriendRequest(DAO):
    def __init__( self, requester, target ):
        self.requester = str(requester)
        self.target = str(target)

    def load( self ):
        result = database_accessor.run_select("SELECT * FROM FriendRequest WHERE " + \
                                            "requester=%s AND target=%s",
                                            self.requester, self.target)
        return bool(result)

    def create( self ):
        return database_accessor.run_change("INSERT INTO FriendRequest VALUES (%s,%s)",
                                            self.requester, self.target)
    
    def remove( self ):
        return database_accessor.run_change("DELETE FROM FriendRequest WHERE " + \
                                            "requester=%s AND target=%s",
                                            self.requester, self.target)

    def update( self ):
        return False


class Account(DAO):
    def __init__( self, account_id ):
        self.id = str(account_id)

    def load( self ):
        return True

    def create( self ):
        return True

    def remove( self ):
        return False

    def update( self ):
        return False

    def get_friendships( self ):
        results = database_accessor.run_select("SELECT * FROM Friendship WHERE " + \
                                              "account1=%s OR account2=%s",
                                              self.id, self.id)
        if not results and results != list(): return False
        
        friendships = list()
        for account1, account2 in results:
            friendship = Friendship(account1,account2)
            friendships.append(friendship)

        return friendships

    def get_friendship( self, search_id ):
        search_id = str(search_id)
        results = database_accessor.run_select("SELECT * FROM Friendship WHERE " + \
                                              "(account1=%s OR account2=%s) " + \
                                              "AND (account1=%s OR account2=%s)",
                                              self.id, self.id,
                                               search_id, search_id)

        if not results: return False
        return Friendship(*(results[0]))

    def get_sent_requests( self ):
        results = database_accessor.run_select("SELECT * FROM FriendRequest WHERE " + \
                                              "requester=%s",
                                              self.id)
        if not results and results != list(): return False
        
        requests = list()
        for requester,target in results:
            request = FriendRequest(requester,target)
            requests.append(request)
        return requests

    def get_received_requests( self ):
        results = database_accessor.run_select("SELECT * FROM FriendRequest WHERE " + \
                                              "target=%s",
                                              self.id)
        if not results and results != list(): return False

        requests = list()
        for requester,target in results:
            request = FriendRequest(requester,target)
            requests.append(request)
        return requests

    def get_sent_request( self, friend_id ):
        requests = self.get_sent_requests()
        if requests:
            requests = [request for request in requests if request.target == str(friend_id)]
            if requests:
                return requests[0]
        return False
        

    def get_received_request( self, friend_id ):
        requests = self.get_received_requests()
        if requests:
            requests = [request for request in requests if request.requester == str(friend_id)]
            if requests:
                return requests[0]
        return False






