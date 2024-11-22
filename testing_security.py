from Security.DatabaseAccessor.DatabaseAccessor import database_accessor
from Security.DAO.Account import Account, AccountView
from Security.CustomerAccessor.CustomerAccessor import CustomerAccessor
import pdb

if __name__ == "__main__":
    test_DAO = True
    if test_DAO:
        # remove initial data
        my_account = Account("me", "password")
        my_account.load()
        my_account.remove()

        my_account = Account("me", "password")
        assert my_account.load() == False
        assert my_account.create() ==  True
        assert my_account.load() == True

        my_account2 = Account("me", "not_password")
        assert my_account2.load() == False
        assert my_account2.create() == False
        assert my_account2.remove() == False

        view = AccountView(userid = my_account.get_id())
        assert view.load() == True

        assert my_account.remove() == True

        assert view.load() == False

    test_CA = False
    if test_CA:
        # create customer accessors for each customer
        c0 = CustomerAccessor()
        c1 = CustomerAccessor()
        c2 = CustomerAccessor()

        c0.create_account("me00", "password00")
        assert c0.login("me00", "password00") == True
        assert bool(c0.get_userid()) == True

        assert c1.login("me00", "password01") == False
        assert c1.get_userid() == False
        assert c1.get_username() == False

        assert c2.get_friend_username(c0.get_userid()) == c0.get_username()
        assert c2.get_friend_id(c0.get_username()) == c0.get_userid()



