from Security.DAO.DAO import DAO
from Security.DatabaseAccessor.DatabaseAccessor import database_accessor
import pdb

class Account(DAO):
    def __init__( self, username, password ):
        self.username = username
        self.password = password
        self.userid = None

    def load( self ):
        result = database_accessor.run_select("SELECT userid FROM SecurityAccount WHERE " + \
                                              "username=%s AND password=%s", 
                                              self.username, self.password)
        if not result: return False

        self.userid = result[0][0]

        return True

    def create( self ):
        result = database_accessor.run_change("INSERT INTO SecurityAccount " + \
                                              "(username,password) VALUES (%s,%s)",
                                            self.username, self.password)
        return bool(result)

    def remove( self ):
        if not self.userid: return False
        return database_accessor.run_change("DELETE FROM SecurityAccount WHERE " + \
                                            "username=%s AND password=%s", 
                                            self.username, self.password)

    def update( self ):
        return False

    def get_id( self ):
        return self.userid


class AccountView(DAO):
    def __init__( self, userid = None, username = None ):
        self.userid = userid
        self.username = username

    def load( self ):
        if self.userid:
            result = database_accessor.run_select("SELECT username FROM SecurityAccount WHERE " + \
                                                  "userid=%s", self.userid)
            if not result: return False
            self.username = result[0][0]

        else:
            result = database_accessor.run_select("SELECT userid FROM SecurityAccount WHERE " + \
                                                  "username=%s", self.username)
            if not result: return False
            self.userid = result[0][0]

        return True

    def create( self ):
        return False

    def remove( self ):
        return False

    def update( self ):
        return False

    def get_username( self ):
        return self.username

    def get_id( self ):
        return self.userid



