from database_accessor import database_accessor as db_accessor

import pdb

# DAO (Database Access Object)
########## Intended Use Cases:
# create, update, load, and remove data from database


########## Keep information in DAO and Database up-to-date
# create: (provides access)
#   adds DAO to the database
#       database:   primary keys    - set to keys in DAO
#                   values          - set to values in DAO
#       DAO:        primary keys    - must not exist in database
#                   values          - 

# load: (provides access)
#   stores database values into DAO
#       database:   primary keys    - 
#                   values          - 
#       DAO:        primary keys    - must exist in database
#                   values          - set to values in database

# update: (requires write access)
#       database:   primary keys    - 
#                   values          - set to values in DAO
#       DAO:        primary keys    - must exist in database
#                   values          - must be non-null

# remove: (requires write access)
#       database:   primary keys    - removed
#                   values          - removed
#       DAO:        primary keys    - must exist in database
#                   values          -


########## modify/read information
# get_<key/value>: (requires read access)
#   returns the specified value from the DAO
# set_<value>: (requires write access)
#   changes the specified value in the DAO
#       NOTE: does not automatically update the database

########## access
# write access:
#   ability to change data in DAO and Database
# read access:
#   ability to read data in DAO and Database

# start with no access
# access can be modified in create() and load()
class DAO:
    # start with no access
    def __init__( self ):
        self._access_remove()
    
    def create( self ):
        raise NotImplemented("Attempted to call abstract method")

    def update( self ):
        raise NotImplemented("Attempted to call abstract method")

    def remove( self ):
        raise NotImplemented("Attempted to call abstract method")

    def load( self ):
        raise NotImplemented("Attempted to call abstract method")

    def write_access( self ):
        return self._write_access

    def read_access( self ):
        return self._read_access

    # full access to DAO
    def _access_set_all( self ):
        self._write_access = True
        self._read_access = True

    # read-only access to DAO
    def _access_set_readonly( self ):
        self._write_access = False
        self._read_access = True

    # no access to DAO
    def _access_remove( self ):
        self._write_access = False
        self._read_access = False

    # sets access to match the DAO source
    def _access_set_by_reference( self, source ):
        self._write_access = source.write_access()
        self._read_access = source.read_access()

    def __str__( self ):
        return f"Write Access: {self._write_access}\nRead Access: {self._read_access}"

# Account (DAO)
##### keys/values
# keys:
#   username - name of the user
# values:
#   password - string to identify account owner
#               * required for write access to account
#               * often acts like a key

##### access
# full access       <- password provided
# read-only access  <- read-only access

##### additions
# get cart:
#   returns cart DAO associated with Account
class Account(DAO):
    def __init__( self, username, password = None ):
        super().__init__()
        self._username = username
        self._password = password

    def get_username( self ):
        if not self._read_access: return False
        return self._username

    # exception: cannot read passowrd without write access
    def get_password( self ):
        if not self._write_access: return False
        return self._password

    def get_cart( self ):
        if not self._read_access: return False
        cart = ShoppingCart(self)
        cart.load()
        return cart

    def set_password( self, password ):
        if self._write_access:
            self._password = password
            return True
        return False

    # automate creation of cart when Account is created
    def create( self ):
        if self._password:
            if db_accessor.run_change(
                    "INSERT INTO Account VALUES (%s,%s)",
                    self._username, self._password ):
                self._access_set_all()
                ShoppingCart(self).create()
                return True
        return False

    def update( self ):
        if not self._write_access: return False
        return db_accessor.run_change(
                "UPDATE Account SET password=%s WHERE username=%s",
                self._password,self._username)

    def remove( self ):
        if not self._write_access: return False
        if self.get_cart().remove():
            db_accessor.run_change(
                    "DELETE FROM Account WHERE username=%s",
                    self._username )
            return True
        return False

    # if password is provided, full access
    # if only username is provided, read-only access
    def load( self ):
        # case password provided
        if self._password:
            if db_accessor.run_select(
                    "SELECT * FROM Account WHERE username=%s AND password=%s",
                    self._username,self._password):
                self._access_set_all()
                return True
        # case no password provided
        else:
            if db_accessor.run_select(
                    "SELECT * FROM Account WHERE username=%s",
                    self._username):
                self._access_set_readonly()
                return True
        return False

# Account (DAO)
##### keys/values
# keys:
#   account - Account that owns the cart

##### access
# access = Account's access

##### other
# get_item_selection: (requires read access)
#   returns list of ItemSelections stored in the cart
# clear: (requires write access)
#   removes all ItemSelections stores from the cart
class ShoppingCart(DAO):
    def __init__( self, account ):
        super().__init__()
        self._account = account

    def get_id( self ):
        if not self._read_access: return False
        return self._account.get_username()

    def create( self ):
        if db_accessor.run_change(
                "INSERT INTO ShoppingCart VALUES (%s)",
                    self._account.get_username()):
            self._access_set_by_reference( self._account )
            return True
        return False

    def update( self ):
        return False

    def remove( self ):
        if self._write_access:
            self.clear()
            if db_accessor.run_change(
                    "DELETE FROM ShoppingCart WHERE id=%s",
                    self.get_id()):
                self._access_remove()
                return True
        return False

    def load( self ):
        if not self._account.write_access(): return False
        self._access_set_by_reference( self._account )
        return True

    # retuns list of all ItemSelections associated with Cart
    # creates ItemSelection DAOs, along with corresponding Item DAOs
    def get_item_selections( self ):
        if not self.read_access(): return False
        # generate a list of data about the selections
        selections = list()
        selection_results = db_accessor.run_select(
                                "SELECT * FROM ItemSelection WHERE cart_id=%s",
                                self.get_id())
        if selection_results:
            # load DAOs from the Data of the ItemSelections
            for item_id,cart_id,quantity in selection_results:
                item = Item(item_id)
                item.load()
                selection = ItemSelection(self,item)
                selection.load()
                selections.append( selection )
        return selections

    # remove all selections associated with this cart
    def clear( self ):
        if not self.write_access(): return False
        for selection in self.get_item_selections():
            selection.remove()

# Item (DAO)
##### keys/values
# keys:
#   item_id - integer id unique to the Item object
#               no significance outside of this system
# values:
#   item_name - value allowing user to recognize item (determined by user, not unique)
#   item_source - link to where the item can be purchased

##### access
# Access = Read-Only
#   prevents customers from modifying data that other customers can use
class Item(DAO):
    def __init__( self, item_id, item_name = None, item_source = None ):
        super().__init__()
        self._id = item_id
        self._name = item_name
        self._source = item_source

    def get_id( self ):
        if not self.read_access(): return False
        return self._id

    def get_name( self ):
        if not self.read_access(): return False
        return self._name

    def set_name( self ):
        if not self._write_access: return False
        raise NotImplemented("Currently write access does not exist for Item\nInstead create a new Item")

    def get_source( self ):
        if not self.read_access(): return False
        return self._source

    def set_source( self ):
        if not self._write_access: return False
        raise NotImplemented("Currently write access does not exist for Item\nInstead create a new Item")

    def create( self ):
        if db_accessor.run_change(
                    "INSERT INTO Item VALUES (%s,%s,%s)",
                    self._id,self._name,self._source):
            self._access_set_readonly()
            return True
        return False

    def load( self ):
        selection_result = db_accessor.run_select(
                                "SELECT * FROM Item WHERE id=%s",
                                self._id)
        if selection_result:
            item_id, item_name, item_source = selection_result[0]
            self._id = item_id
            self._name = item_name
            self._source = item_source
            self._access_set_readonly()
            return True
        return False

    # update/remove:
    #   due to not having write access, chose to skip implementation
    def update( self ):
        if not self._write_access: return False
        raise NotImplemented("Currently write access does not exist for Item\nInstead create a new Item")

    def remove( self ):
        if not self._write_access: return False
        raise NotImplemented("Currently write access does not exist for Item\nInstead create a new Item")

# ItemSelection (DAO)
##### keys/values
# keys:
#   cart - Cart that the ItemSelection belongs to
#   item - Item that is being selected by the cart
# values:
#   quantity - amount of items stored in the cart

##### access
# access = Cart's access
class ItemSelection( DAO ):
    def __init__( self, cart, item, quantity = None ):
        super().__init__()
        self._cart = cart
        self._item = item
        self._quantity = quantity

    def get_cart( self ):
        if not self.read_access(): return False
        return self._cart
    
    def get_item( self ):
        if not self.read_access(): return False
        return self._item

    def get_quantity( self ):
        if not self.read_access(): return False
        return self._quantity

    def set_quantity( self, quantity ):
        if not self._write_access(): return False
        self._quantity = quantity

    def create( self ):
        if db_accessor.run_change(
                    "INSERT INTO ItemSelection VALUES (%s,%s,%s)",
                    self._item.get_id(),self._cart.get_id(),self._quantity):
            self._access_set_by_reference( self._cart )
            return True
        return False

    def load( self ):
        selection_result = db_accessor.run_select(
                    "SELECT * FROM ItemSelection WHERE item_id=%s AND cart_id=%s",
                    self._item.get_id(),self._cart.get_id())
        if selection_result:
            item_id,cart_id,quantity = selection_result[0]
            self._quantity = quantity
            self._access_set_by_reference( self._cart )
            return True
        return False

    def update( self ):
        if not self._write_access: return False
        return db_accessor.run_change(
                    "UPDATE ItemSelection SET quantity=%s WHERE cart_id=%s AND item_id=%s",
                    self.get_quantity(),
                    self.get_cart().get_id(),
                    self.get_item().get_id())

    def remove( self ):
        if not self._write_access: return False
        if db_accessor.run_change(
                    "DELETE FROM ItemSelection WHERE cart_id=%s AND item_id=%s",
                    self.get_cart().get_id(),self.get_item().get_id()):
            self._access_remove()
            return True
        return False

# clear database
# NOTE: this method is for testing only
#       running sql commands outside of DAO should not be necessary
def clear_database_TESTING():
    # clear accounts
    select_result = db_accessor.run_select( "SELECT * FROM Account" )
    if select_result:
        for username,password in select_result:
            account = Account(username,password)
            account.load()
            account.remove()

    # clear items
    select_result = db_accessor.run_select( "SELECT id FROM Item" )
    if select_result:
        for item_id in select_result:
            item = Item(item_id)
            item.load()
            item.remove()
        

if __name__ == "__main__":
    test_accounts = True
    if test_accounts:
        # run 1: new account with new password
        print( "First Run: New Password" )
        my_account = Account("Michael", "my_password")
        assert my_account.load() == False
        assert my_account.create() == True
        assert my_account.set_password("other_password") == True
        assert my_account.update() == True

        # run 2: attempt to reaccess account with correct password
        print( "Second Run: Correct Password" )
        second_account = Account("Michael", "other_password")
        assert second_account.load() == True
        assert second_account.create() == False
        assert second_account.set_password("***********") == True
        assert second_account.update() == True

        # run 3: attempt to reaccess account with incorrect password
        print( "Third Run: Incorrect Password" )
        third_account = Account("Michael", "******")
        assert third_account.load() == False
        assert third_account.create() == False
        assert third_account.set_password("******") == False
        assert third_account.update() == False

        # run 4: attempt to reaccess account with correct password
        #           verify data was not modified during by run 3
        print( "Verify Password" )
        fourth_account = Account("Michael", "***********")
        fourth_account.load()
        assert fourth_account.get_password() == "***********"

        # clear data
        print( "Remove Account" )
        assert my_account.remove() == True

    test_selections = True
    if test_selections:
        print( "Create selection" )
        # create Michael's item
        my_account = Account("Michael", "my_password")
        assert my_account.create() == True

        my_cart = ShoppingCart( my_account )
        assert my_cart.load() == True

        my_item = Item(42,"My Item","https://my_source.com")
        if not my_item.load():
            assert my_item.create() == True
        assert my_item.load() == True

        my_selection = ItemSelection( my_cart, my_item, quantity = 5 )
        assert my_selection.create() == True

        print( "Access selection" )
        # access Michael's item
        my_account = Account("Michael", "my_password")
        assert my_account.load() == True
        my_cart = ShoppingCart( my_account )
        assert my_cart.load() == True

        my_item = Item(42)
        assert my_item.load() == True

        my_selection = ItemSelection( my_cart, my_item )
        assert my_selection.load() == True
        assert my_selection.get_quantity() == 5 # verify correct amount

        # delete Michael's account
        assert my_account.remove() == True




