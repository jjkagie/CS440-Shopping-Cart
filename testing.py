#from backend_code.DAO import Account, ShoppingCart, ItemSelection, Item, pause_connection
from backend_code.customer_accessor import customer_accessor
from backend_code.DAO import pause_connection


if __name__ == "__main__":
    # Account:
    #   username = "Michael"
    #   password = "my_password"

    # 1. create a customer_accessor to interact with backend
    me = customer_accessor()
    # 2. create an account
    me.create_account("Michael", "my_password")
    # 3. login to the account
    me.login("Michael", "my_password")
    # 4. create items
    #   (current version automatically adds them to cart)
    me.create_item("my_item", "my_source.com", 5)
    me.create_item("my_large_item", "my_large_source.com", 4)
    
    # 5. add the items to the cart
        # cannot implement with the style due to event-driven architecture
        # alternative: customer_accessor.on_get_item_selections()
        #               allows user to select an item object,
        #               which is used to call add/delete item
    #assert me.add_item_to_cart(my_item, 42) == True
    #assert me.add_item_to_cart(my_item_large, 1) == True
    
    # print the items that were added to the cart
    me.get_item_selections()

        # cannot implement with the style due to event-driven architecture
        # alternative: customer_accessor.on_get_item_selections()
        #               allows user to select an item object,
        #               which is used to call add/delete item
    # 6. remove items from the cart
    #me.remove_item_from_cart(my_item)
    
    # print updated list of items in cart
    me.get_item_selections()

    # delete the account (optional)
    me.delete_account()

    pause_connection()









