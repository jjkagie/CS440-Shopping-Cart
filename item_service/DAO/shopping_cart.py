from .DAO import DAO
from DatabaseAccessor.database_accessor import database_accessor as db_accessor



class ShoppingCart(DAO):
    def __init__( self, username ):
        super().__init__()
        self._account = username

    def get_id( self ):
        #if not self._read_access: return False
        return self._account

    def create( self ):
        if db_accessor.run_change(
                "INSERT INTO ShoppingCart VALUES (%s)",
                    self._account):
            #self._access_set_by_reference( self._account )
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
        if not self._account.read_access(): return False
        #self._access_set_by_reference( self._account )
        return True

    # retuns list of all ItemSelections associated with Cart
    # creates ItemSelection DAOs, along with corresponding Item DAOs
    def get_item_selections( self ):
        #if not self.read_access(): return False
        # generate a list of data about the selections
        selections = list()
        selection_results = db_accessor.run_select(
                                "SELECT * FROM ItemSelection WHERE cart_id=%s",
                                self.get_id())
        if selection_results:
            # load DAOs from the Data of the ItemSelections
            for item_name,item_source,cart_id,quantity in selection_results:
                item = Item(item_name,item_source)
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
#   item_name - short name of the item (not necessarily unique)
#   item_source - link to where the item can be purchased
# values:
#   item_name - value allowing user to recognize item (determined by user, not unique)
#   item_source - link to where the item can be purchased

##### access
# Access = Read-Only
#   prevents customers from modifying data that other customers can use
class Item(DAO):
    def __init__( self, item_name, item_source ):
        super().__init__()
        self._name = item_name
        self._source = item_source

    def get_name( self ):
        if not self.read_access(): return False
        return self._name

    def get_source( self ):
        if not self.read_access(): return False
        return self._source

    def create( self ):
        if db_accessor.run_change(
                    "INSERT INTO Item VALUES (%s,%s)",
                    self._name,self._source):
            self._access_set_readonly()
            return True
        return False

    def load( self ):
        selection_result = db_accessor.run_select(
                                "SELECT * FROM Item WHERE item_name=%s AND item_source=%s",
                                self._name,self._source)
        if selection_result:
            item_name, item_source = selection_result[0]
            self._name = item_name
            self._source = item_source
            self._access_set_readonly()
            return True
        return False

    def update( self ):
        if not self._write_access: return False
        raise False # Item does not have values to change

    def remove( self ):
        if not self._write_access: return False
        db_accessor.run_change("DELETE FROM Item WHERE item_name=%s AND item_source=%s",
                               self.get_name(),self.get_source())


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
        #if not self.read_access(): return False
        return self._cart
    
    def get_item( self ):
        #if not self.read_access(): return False
        return self._item

    def get_quantity( self ):
       #if not self.read_access(): return False
        return self._quantity

    def set_quantity( self, quantity ):
        #if not self._write_access(): return False
        self._quantity = quantity

    def create( self ):
        if db_accessor.run_change(
                    "INSERT INTO ItemSelection VALUES (%s,%s,%s,%s)",
                    self._item.get_name(),self._item.get_source(),
                    self._cart.get_id(),self._quantity):
            #self._access_set_by_reference( self._cart )
            return True
        return False

    def load( self ):
        selection_result = db_accessor.run_select(
                    "SELECT * FROM ItemSelection WHERE item_name=%s AND item_source=%s"
                    " AND cart_id=%s",
                    self._item.get_name(),self._item.get_source(),
                    self._cart.get_id())
        if selection_result:
            item_name,item_source,cart_id,quantity = selection_result[0]
            self._quantity = quantity
            #self._access_set_by_reference( self._cart )
            return True
        return False

    def update( self ):
        #if not self._write_access: return False
        return db_accessor.run_change(
                    "UPDATE ItemSelection SET quantity=%s WHERE cart_id=%s "
                    "AND item_name=%s AND item_source=%s",
                    self.get_quantity(),
                    self.get_cart().get_id(),
                    self.get_item().get_name(),self.get_item.get_source())

    def remove( self ):
        #if not self._write_access: return False
        if db_accessor.run_change(
                    "DELETE FROM ItemSelection WHERE cart_id=%s AND item_name=%s AND item_source=%s",
                    self.get_cart().get_id(),
                    self.get_item().get_name(),self.get_item().get_source()):
            self._access_remove()
            return True
        return False