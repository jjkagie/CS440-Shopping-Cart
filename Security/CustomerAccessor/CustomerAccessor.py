from Security.DAO.Account import Account, AccountView

class CustomerAccessor:
    def __init__( self ):
        self.account = None

    def create_account( self, username, password ):
        account = Account( username, password )
        return account.create()

    def login( self, username, password ):
        account = Account(username, password)
        if account.load():
            self.account = account
            return True
        return False

    def get_username( self ):
        if self.account:
            return self.account.get_username()
        return False

    def get_userid( self ):
        if self.account:
            return self.account.get_id()
        return False

    def get_friend_username( self, userid ):
        account = AccountView( userid = userid )
        account.load()
        return account.get_username()

    def get_friend_userid( self, username ):
        account = AccountView( username = username )
        account.load()
        return account.get_id()




