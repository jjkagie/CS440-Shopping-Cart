from database_accessor import database_accessor as db_accessor

import pdb



class DAO:
    def __init__( self ):
        self._write_access = False
        self._read_access = False
    
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
        
    def _access_set_all( self ):
        self._write_access = True
        self._read_access = True

    def _access_set_readonly( self ):
        self._write_access = False
        self._read_access = True

    def _access_remove( self ):
        self._write_access = False
        self._read_access = False

    def _access_set_by_reference( self, source ):
        self._write_access = source.write_access()
        self._read_access = source.read_access()

    def __str__( self ):
        return f"Write Access: {self._write_access}\nRead Access: {self._read_access}"

class Account(DAO):
    def __init__( self, username, password = None ):
        super().__init__()
        self._username = username
        self._password = password

    def get_username( self ):
        if not self._read_access: return False
        return self._username

    def get_password( self ):
        if not self._write_access: return False
        return self._password

    def set_password( self, password ):
        if self._write_access:
            self._password = password
            return True
        return False

    def create( self ):
        if self._password:
            sql = "INSERT INTO Account VALUES (%s,%s)"
            create_tuple = (self._username,self._password)
            if db_accessor.run_change( sql, create_tuple ):
                self._access_set_all()
                return True
        return False

    def update( self ):
        if not self._write_access: return False
        sql = "UPDATE Account SET password=%s WHERE username=%s"
        update_tuple = (self._password,self._username)
        return db_accessor.run_change(sql,update_tuple)

    def remove( self ):
        if not self._write_access: return False
        sql = "DELETE FROM Account WHERE username=%s"
        remove_tuple = (self._username,)
        if db_accessor.run_change( sql, remove_tuple ):
            self._access_remove()
            return True
        return False

    def load( self ):
        # intent = read and write
        if self._password:
            sql = "SELECT * FROM Account WHERE username=%s AND password=%s"
            load_tuple = (self._username,self._password)
            if db_accessor.run_select(sql,load_tuple):
                self._access_set_all()
                return True
        # intent = write only
        else:
            sql = "SELECT * FROM Account WHERE username=%s"
            load_tuple = (self._username,)
            if db_accessor.run_select(sql,load_tuple):
                self._access_set_readonly()
                return True
        return False

class ShoppingCart(DAO):
    def __init__( self, account ):
        super().__init__()
        self._account = account

    def get_id( self ):
        if not self._read_access: return False
        return self._account.get_username()

    def create( self ):
        sql = "INSERT INTO ShoppingCart VALUES (%s)"
        create_tuple = (self._account.get_username(),)
        if db_accessor.run_change(sql,create_tuple):
            self._access_set_by_reference( self._account )
            return True
        return False

    def update( self ):
        return False

    def remove( self ):
        if self._write_access:
            sql = "DELETE FROM ShoppingCart WHERE id=%s"
            remove_tuple = (self.get_id(),)
            if db_accessor.run_change(sql,remove_tuple):
                self._access_remove()
                return True
        return False

    def load( self ):
        if not self._account.write_access(): return False
        self._access_set_by_reference( self._account )
        return True


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
        sql = "INSERT INTO Item VALUES (%s,%s,%s)"
        create_tuple = (self._id,self._name,self._source)
        if db_accessor.run_change(sql,create_tuple):
            self._access_set_readonly()
            return True
        return False

    def load( self ):
        sql = "SELECT * FROM Item WHERE id=%s"
        load_tuple = (self._id,)
        selection_result = db_accessor.run_select(sql,load_tuple)
        if selection_result:
            item_id, item_name, item_source = selection_result[0]
            self._id = item_id
            self._name = item_name
            self._source = item_source
            self._access_set_readonly()
            return True
        return False

    def update( self ):
        if not self._write_access: return False
        raise NotImplemented("Currently write access does not exist for Item\nInstead create a new Item")

    def remove( self ):
        if not self._write_access: return False
        raise NotImplemented("Currently write access does not exist for Item\nInstead create a new Item")

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
        sql = "INSERT INTO ItemSelection VALUES (%s,%s,%s)"
        create_tuple = (self._item.get_id(),self._cart.get_id(),self._quantity)
        if db_accessor.run_change(sql,create_tuple):
            self._access_set_by_reference( self._cart )
            return True
        return False

    def load( self ):
        sql = "SELECT * FROM ItemSelection WHERE item_id=%s AND cart_id=%s"
        load_tuple = (self._item.get_id(),self._cart.get_id())
        selection_result = db_accessor.run_select(sql,load_tuple)
        if selection_result:
            item_id,cart_id,quantity = selection_result[0]
            self._quantity = quantity
            self._access_set_by_reference( self._cart )
            return True
        return False

    def update( self ):
        if not self._write_access: return False
        sql = "UPDATE ItemSelection SET quantity=%s WHERE cart_id=%s AND item_id=%s"
        update_tuple = (self.get_quantity(),self.get_cart().get_id(),
                        self.get_item().get_id())
        return db_accessor.run_change(sql,update_tuple)

    def remove( self ):
        if not self._write_access: return False
        sql = "DELETE FROM ItemSelection WHERE cart_id=%s AND item_id=%s"
        remove_tuple = (self.get_cart().get_id(),self.get_item().get_id())
        if db_accessor.run_change( sql, remove_tuple ):
            self._access_remove()
            return True
        return False


if __name__ == "__main__":
    test_accounts = True
    if test_accounts:
        print( "First Run: New Password" )
        my_account = Account("Michael", "my_password")
        assert my_account.load() == False
        assert my_account.create() == True
        assert my_account.set_password("other_password") == True
        assert my_account.update() == True

        print( "Second Run: Correct Password" )
        second_account = Account("Michael", "other_password")
        assert second_account.load() == True
        assert second_account.create() == False
        assert second_account.set_password("***********") == True
        assert second_account.update() == True

        print( "Third Run: Incorrect Password" )
        third_account = Account("Michael", "******")
        assert third_account.load() == False
        assert third_account.create() == False
        assert third_account.set_password("******") == False
        assert third_account.update() == False

        print( "Verify Password" )
        fourth_account = Account("Michael", "***********")
        fourth_account.load()
        assert fourth_account.get_password() == "***********"
        
        print( "Remove Account" )
        assert my_account.remove() == True

    test_selections = True
    if test_selections:
        print( "Create selection" )
        # create Michael's Pizza
        my_account = Account("Michael", "my_password")
        assert my_account.create() == True

        # TODO: automatically generate cart on account creation
        my_cart = ShoppingCart( my_account )
        assert my_cart.create() == True

        my_item = Item(42,"My Item","https://my_source.com")
        if not my_item.load():
            assert my_item.create() == True
        assert my_item.load() == True

        my_selection = ItemSelection( my_cart, my_item, quantity = 5 )
        assert my_selection.create() == True

        print( "Access selection" )
        # access Michael's Pizza
        my_account = Account("Michael", "my_password")
        assert my_account.load() == True
        my_cart = ShoppingCart( my_account )
        assert my_cart.load() == True

        my_item = Item(42)
        assert my_item.load() == True

        my_selection = ItemSelection( my_cart, my_item )
        assert my_selection.load() == True
        assert my_selection.get_quantity() == 5 # verify correct amount
        assert my_selection.remove() == True

        # delete Michael's account
        # ERROR: must delete ShoppingCart first
        #assert my_account.remove() == True
        db_accessor.run_change( "DELETE FROM ItemSelection WHERE cart_id=%s", ("Michael",) )
        db_accessor.run_change( "DELETE FROM ShoppingCart WHERE id=%s", ("Michael",) )
        db_accessor.run_change( "DELETE FROM Account WHERE username=%s", ("Michael",) )
        db_accessor.run_change( "DELETE FROM Item WHERE id=%s", ("42",) )






