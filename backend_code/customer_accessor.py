from DAO import Account, ShoppingCart, ItemSelection, Item
import pdb

# temporary function - need more effecient process
# returns an id that is not already used by an item
def get_unused_item_id():
    item_id = 1
    while True:
        item = Item(item_id)
        if not item.load():
            return item_id
        item_id += 1
    return False

# class intended to interact with user
class customer_accessor:
    # account: account that customer is currently viewing/logged into
    # cart: account's cart
    _account = None
    _cart = None
    
    def __init__( self ):
        pass

    # creates an account if it does not already exist
    # returns if the account's creation was successful
    def create_account(self, username, password):
        self._account = Account(username,password)
        return self._account.create()

    # logs into the account, and accesses its cart
    # returns if the login was successful
    def login(self, username, password):
        self._account = Account(username,password)
        if self._account.load():
            self._cart = ShoppingCart(self._account)
            return self._cart.load()
        return False

    # views the account of a user, and accesses its cart
    # returns if able to view the account
    def view_account(self, username):
        self._account = Account(username)
        if self._account.load():
            self._cart = ShoppingCart(account)
            return self._cart.load()
        return False

    # if logged in, adds <quantity> items to the cart
    # returns if addition was sucecssful
    def add_item_to_cart(self, item, quantity):
        if self._cart:
            item_selection = ItemSelection(self._cart, item, quantity)
            return item_selection.create()
        return False

    # if logged in, removes item from the cart
    # returns if removal was sucecssful
    def remove_item_from_cart(self, item):
        if self._cart:
            item_selection = ItemSelection(self._cart, item)
            item_selection.load()
            return item_selection.remove()
        return False

    # if logged in or viewing, returns a list of the cart's ItemSelections
    # otherwise, returns False
    def get_item_selections(self):
        if self._cart:
            return self._cart.get_item_selections()
        return False

    # if logged in, deletes the account
    # returns if deletion was successful
    def delete_account(self):
        if self._account:
            return self._account.remove()
        return True

    # creates an item with the specified name and source
    # returns the created item, or False for failure to create
    def create_item(self, item_name, item_source):
        item = Item(get_unused_item_id(), item_name, item_source)
        if item.create():
            return item
        return False

    # if logged in or viewing, print all items in the cart
    def view_item_selections(self):
        selections = self.get_item_selections()
        print( "Selections Display:" )
        if selections:
            for selection in selections:
                item = selection.get_item()
                print( f"{item.get_name()} from {item.get_source()} ({selection.get_quantity()})")
        print()
        


if __name__ == "__main__":
    # Account:
    #   username = "Michael"
    #   password = "my_password"

    # 1. create a customer_accessor to interact with backend
    me = customer_accessor()
    # 2. create an account
    assert me.create_account("Michael", "my_password") == True
    # 3. login to the account
    assert me.login("Michael", "my_password") == True
    # 4. create items, (will implement tools to identify existing items later)
    my_item = me.create_item("my_item", "my_source.com")
    my_item_large = me.create_item("my_large_item", "my_large_source.com")
    # 5. add the items to the cart
    assert me.add_item_to_cart(my_item, 42) == True
    assert me.add_item_to_cart(my_item_large, 1) == True
    # print the items that were added to the cart
    me.view_item_selections()
    # 6. remove items from the cart
    assert me.remove_item_from_cart(my_item)
    # print updated list of items in cart
    me.view_item_selections()

    # delete the account (optional)
    assert me.delete_account() == True


