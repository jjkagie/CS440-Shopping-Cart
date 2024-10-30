from .DAO import Account, ShoppingCart, ItemSelection, Item, pause_connection
from Broker.Broker import broker_ca
import pdb


# class intended to interact with user
class customer_accessor:
    # account: account that customer is currently viewing/logged into
    # cart: account's cart
    _account = None
    _cart = None
    
    def __init__( self ):
        broker_ca.subscribe( self, self )

    # creates an account if it does not already exist
    # returns if the account's creation was successful
    def create_account(self, username, password):
        account = Account(username,password)
        result = account.create()
        
        broker_ca.publish_create_account(publisher=self,
                                         was_successful=result)
    
    # logs into the account, and accesses its cart
    # returns if the login was successful
    def login(self, username, password):
        account = Account(username,password)
        result = False
        if account.load():
            self._account = account
            self._cart = ShoppingCart(self._account)
            result = self._cart.load()
        
        broker_ca.publish_login(publisher=self,
                                was_successful=result)

    # views the account of a user, and accesses its cart
    # returns if able to view the account
    def view_account(self, username):
        account = Account(username)
        result = False
        if account.load():
            self._account = account
            self._cart = ShoppingCart(account)
            result = self._cart.load()

        broker_ca.publish_view_account(publisher=self,
                                       was_sucessful=result)
    
    # if logged in, adds <quantity> items to the cart
    # returns if addition was sucecssful
    def add_item_to_cart(self, item, quantity):
        result = False
        if self._cart:
            item_selection = ItemSelection(self._cart, item, quantity)
            result = item_selection.create()

        broker_ca.publish_add_item_to_cart(publisher=self,
                                           was_successful=result)

    # if logged in, removes item from the cart
    # returns if removal was sucecssful
    def remove_item_from_cart(self, item):
        result = False
        if self._cart:
            item_selection = ItemSelection(self._cart, item)
            item_selection.load()
            result = item_selection.remove()
        
        broker_ca.publish_remove_item_from_cart(publisher=self,
                                           was_successful=result)

    # if logged in or viewing, returns a list of the cart's ItemSelections
    # otherwise, returns False
    def get_item_selections(self):
        result = False
        if self._cart:
            result = self._cart.get_item_selections()

        broker_ca.publish_get_item_selections(publisher=self,
                                           selections=result)
    
    # if logged in, deletes the account
    # returns if deletion was successful
    def delete_account(self):
        result = False
        if self._account:
            result = self._account.remove()

        broker_ca.publish_delete_account(publisher=self,
                                         was_successful=result)

    # creates an item with the specified name and source
    # returns the created item, or False for failure to create
    def create_item(self, item_name, item_source, quantity):
        item = Item(item_name, item_source)
        if item.create():
            result = item
        elif item.load():
            result = item
        else:
            result = False

        broker_ca.publish_create_item(publisher=self,
                                         item=result,
                                      quantity=quantity)

        # cannot implement with this style due to event-driven architecture
    # if logged in or viewing, print all items in the cart
    #def view_item_selections(self):
    #    selections = self.get_item_selections()
    #    print( "Selections Display:" )
    #    if selections:
    #        for selection in selections:
    #            item = selection.get_item()
    #            print( f"{item.get_name()} from {item.get_source()} (x{selection.get_quantity()})")
    #    print()
        



    # subscriber methods:
    # called when self finishes the action
    #   rewrite these as needed
    def on_create_account(self, was_successful):
        print( f"\nCreate Account attempt = {was_successful}" )

    def on_login(self, was_successful):
        print( f"\nLogin attempt = {was_successful}" )

    def on_view_account(self, was_successful):
        print( f"\nView Account atttempt = {was_successful}" )

    def on_add_item_to_cart(self, was_successful):
        print( f"\nAdd Item attempt = {was_successful}" )

    def on_get_item_selections(self, selections):
        if selections:
            print( "\n\nItem Selections Display:" )
            for selection in selections:
                item = selection.get_item()
                print( f"{item.get_name()} from {item.get_source()} " + \
                       f"(x{selection.get_quantity()})")
            print()
        else:
            print( f"\nGet Item Selections attempt = {False}" )

    def on_remove_item_from_cart(self, was_successful):
        print( f"\nRemove Item attempt = {was_successful}" )

    def on_delete_account(self, was_successful):
        print( f"\nDelete Account attempt = {was_successful}" )

    def on_create_item(self, item, quantity):
        if item:
            print( f"\nItem Created: {item.get_name()} -> {item.get_source()}" )
            print( f"Automatically adding {quantity} to cart" )
            self.add_item_to_cart(item, quantity)
        else:
            print( f"\nItem Created attempt = {False}" )

    # currently customer_acccessor does not subscribe to broker_dao
    #   no need to implement these methods
    def on_change(self, dao_id, values):
        pass

    def on_delete(self, dao_id):
        pass

        
        
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
    assert me.remove_item_from_cart(my_item) == True
    # print updated list of items in cart
    me.view_item_selections()

    # delete the account (optional)
    assert me.delete_account() == True

    pause_connection()


