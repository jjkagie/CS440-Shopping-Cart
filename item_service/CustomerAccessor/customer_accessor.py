from DAO.shopping_cart import ShoppingCart, ItemSelection, Item, db_accessor

class item_accessor:
    def __init__(self, username):
        self._cart = ShoppingCart(username)


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
            result = self._cart.get_item_selections()
        return result
    
    # creates an item with the specified name and source
    # returns the created item, or False for failure to create
    def create_item(self, item_name, item_source):
        item = Item(item_name, item_source)
        if item.create():
            return item
        elif item.load():
            return item
        return False

    # if logged in or viewing, print all items in the cart
    def view_item_selections(self):
        selections = self.get_item_selections()
        print( "Selections Display:" )
        if selections:
            for selection in selections:
                item = selection.get_item()
                print( f"{item.get_name()} from {item.get_source()} (x{selection.get_quantity()})")
        print()