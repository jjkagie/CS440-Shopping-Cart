from DAO import Account, ShoppingCart, ItemSelection, Item
import pdb

# temporary function - need more effecient process
def get_unused_item_id():
    item_id = 1
    while True:
        item = Item(item_id)
        if not item.load():
            return item_id
        item_id += 1
    return False


class customer_accessor:
    _account = None
    _cart = None
    
    def __init__( self ):
        pass

    def create_account(self, username, password):
        self._account = Account(username,password)
        return self._account.create()

    def login(self, username, password):
        self._account = Account(username,password)
        if self._account.load():
            self._cart = ShoppingCart(self._account)
            return self._cart.load()
        return False

    def view_account(self, username):
        self._account = Account(username)
        if self._account.load():
            self._cart = ShoppingCart(account)
            return self._cart.load()
        return False

    def add_item_to_cart(self, item, quantity):
        if self._cart:
            item_selection = ItemSelection(self._cart, item, quantity)
            return item_selection.create()
        return False

    def remove_item_from_cart(self, item):
        if self._cart:
            item_selection = ItemSelection(self._cart, item)
            item_selection.load()
            return item_selection.remove()
        return False

    def get_item_selections(self):
        if self._cart:
            return self._cart.get_item_selections()
        return False

    def delete_account(self):
        if self._account:
            return self._account.remove()
        return True

    def create_item(self, item_name, item_source):
        item = Item(get_unused_item_id(), item_name, item_source)
        if item.create():
            return item
        return False

    def view_item_selections(self):
        selections = self.get_item_selections()
        print( "Selections Display:" )
        if selections:
            for selection in selections:
                item = selection.get_item()
                print( f"{item.get_name()} from {item.get_source()} ({selection.get_quantity()})")
        print()
        


if __name__ == "__main__":
    me = customer_accessor()
    assert me.create_account("Michael", "my_password") == True
    assert me.login("Michael", "my_password") == True
    my_item = me.create_item("my_item", "my_source.com")
    my_item_large = me.create_item("my_large_item", "my_large_source.com")
    assert me.add_item_to_cart(my_item, 42) == True
    assert me.add_item_to_cart(my_item_large, 1) == True
    me.view_item_selections()
    assert me.remove_item_from_cart(my_item)
    me.view_item_selections()


    assert me.delete_account() == True


