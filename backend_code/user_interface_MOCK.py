from customer_accessor import Item, pause_connection, customer_accessor
import pdb


class SelectionNode:
    # _parent: SelectionNode that created self
    # _children: All SelectionNodes self can create
    # _access_prompt: Displayed when user is viewing parent's children
    # _title: Displayed when self.begin() is called

    def __init__( self, parent = None,
                  title = "TITLE_NOT_SET",
                  access_prompt = "ACCESS_PROMPT_NOT_SET"):
        self.__UA = None
        self._parent = parent
        self._access_prompt = access_prompt
        self._title = title
        self.force_quit = False # TODO: create separate class for single/multi search
        self.get_UA()

    def _generate_children_nodes( self ):
        return list()

    def begin( self ):
        children = self._generate_children_nodes()
        num_options = len( children )

        while True:
            if self.force_quit:
                return True # TODO: create separate class for single/multi search
            
            print( "\n" + str(self) )
            for child_ind,child_node in enumerate(children):
                print( f"{child_ind+1}: {child_node._access_prompt}" )

            try:
                user_input = input( "\nEnter a selection or [q]uit: " )
                selection_index = int( user_input ) - 1
                selected_child = children[ selection_index ]
            except:
                if user_input and user_input[0].lower() == 'q':
                    return True
                print( f"Invalid Selection: Must be between {1} and {num_options}" )
                continue

            selected_child.begin()

    # get user accessor
    # first searches self, then searches parent, then creates a new instance
    def get_UA( self ):
        if self.__UA:
            pass
        elif self._parent:
            self.__UA = self._parent.get_UA()
        else:
            self.__UA = customer_accessor()
        return self.__UA

    # displays the progress in the selection system
    def __str__( self ):
        if self._parent:
            return str(self._parent) + " -> " + self._title
        return self._title


############# Starting Menu ###########
class Selection_LoginMenu(SelectionNode):
    def __init__( self, parent = None ):
        super().__init__( parent = parent, 
                          title = "Login Menu",
                          access_prompt = "Login" )

    def _generate_children_nodes( self ):
        children = [Selection_Login(parent=self),
                    Selection_View(parent=self),
                    Selection_CreateAccount(parent=self)]
        return children

############# Access Actions ###########
# Attempting to create account
class Selection_CreateAccount(SelectionNode):
    def __init__( self, parent = None ):
        super().__init__( parent = parent, 
                          title = "Create Account",
                          access_prompt = "Create Account" )

    def begin( self ):
        print( "\n" + str(self) )
        username = input( "Username: " )
        password = input( "Password: " )
        if not self.get_UA().create_account( username, password ):
            print( "ERROR: Unable to create account" )
            return True
        print( "Account Created Successfully" )
        return True

# Attempting to log into account
class Selection_Login(SelectionNode):
    def __init__( self, parent = None ):
        super().__init__( parent = parent, 
                          title = "Login to Account",
                          access_prompt = "Login to Account" )

    def begin( self ):
        # first, get username and password
        print( "\n" + str(self) )
        username = input( "Username: " )
        password = input( "Password: " )
        if not self.get_UA().login( username, password ):
            print( "ERROR: Unable to login to account" )
            return True
        # after, begin the logged in selections
        return Selection_LoggedIn(parent=self).begin()

# Attmpting to view account
class Selection_View(SelectionNode):
    def __init__( self, parent = None ):
        super().__init__( parent = parent, 
                          title = "View Account",
                          access_prompt = "View Account" )

    # first, get username
    def begin( self ):
        print( "\n" + str(self) )
        username = input( "Username: " )
        if not self.get_UA().view_account( username ):
            print( "ERROR: Unable to view account" )
            return True
        # after, begin the viewing selections
        return Selection_Viewing(parent=self).begin()




    

############# Generic Actions ###########
# Already logged into account
class Selection_LoggedIn(SelectionNode):
    def __init__( self, parent = None ):
        super().__init__( parent = parent, 
                          title = "Logged into Account",
                          access_prompt = "Already Logged In" )

    def _generate_children_nodes( self ):
        children = [Selection_AddItem(self),Selection_RemoveItem(self),
                    Selection_ViewSelections(self),Selection_RemoveAccount(self)]
        return children

# Already Viewing account
class Selection_Viewing(SelectionNode):
    def __init__( self, parent = None ):
        super().__init__( parent = parent, 
                          title = "Viewing Account",
                          access_prompt = "Already Viewing Account" )

    def _generate_children_nodes( self ):
        children = [Selection_ViewSelections(self)]
        return children






################ Specific Actions ###############
# add item
# when an item is selected, on_item_selected must be called
class Selection_AddItem(SelectionNode):
    def __init__( self, parent = None ):
        super().__init__( parent = parent, 
                          title = "Adding Item",
                          access_prompt = "Add Item" )
        self.selected_item = None

    def _generate_children_nodes( self ):
        children = [Selection_SelectItem(self),Selection_CreateItem(self)]
        return children

    def begin( self ):
        self.force_quit = False
        super().begin()
        if self.selected_item:
            quantity = input( "Quantity: " )
            if not self.get_UA().add_item_to_cart(self.selected_item,quantity):
                print( "Unable to add item" )
        return True

    def on_item_selected( self, selected_item ):
        self.selected_item = selected_item
        self.force_quit = True # terminate super().begin() when item is selected


# remove item
# when an item is selected, on_item_selected must be called
class Selection_RemoveItem(SelectionNode):
    def __init__( self, parent = None ):
        super().__init__( parent = parent, 
                          title = "Removing Item",
                          access_prompt = "Remove Item" )
        self.selected_item = None

    def _generate_children_nodes( self ):
        children = [Selection_SelectItem(self)]
        return children

    def begin( self ):
        Selection_SelectItem(self).begin()
        if self.selected_item:
            self.get_UA().remove_item_from_cart(self.selected_item)

    def on_item_selected( self, selected_item ):
        self.selected_item = selected_item


# view items
class Selection_ViewSelections(SelectionNode):
    def __init__( self, parent = None ):
        super().__init__( parent = parent, 
                          title = "Viewing Items",
                          access_prompt = "View Items" )

    def _generate_children_nodes( self ):
        children = [Selection_ViewSelections(self)]
        return children

    def begin( self ):
        self.get_UA().view_item_selections()
        input( "press enter to continue" )
        return True

class Selection_RemoveAccount(SelectionNode):
    def __init__( self, parent = None ):
        super().__init__( parent = parent, 
                          title = "DELETING ACCOUNT",
                          access_prompt = "DELETE ACCOUNT" )

    def begin( self ):
        print( "\n" + str(self) )
        print( "\nThis will delete your account permanently. \nThis action cannot be undone. " )
        user_input = input( "To confirm: type 'CONFIRM': " )
        if user_input == "CONFIRM":
            if self.get_UA().delete_account():
                print( "Account Deleted Successfully" )
                # force quit everything
                parent = self._parent
                while parent:
                    parent.force_quit = True
                    parent = parent._parent
            else:
                print( "Failed to delete account" )
        else:
            print( f"'{user_input}' does not match 'CONFIRM': Aborting" )
        return True
                

################### Item Access ###############
# create item
class Selection_CreateItem(SelectionNode):
    def __init__( self, parent = None ):
        super().__init__( parent = parent, 
                          title = "Creating Item",
                          access_prompt = "Create Item" )

    def begin(self):
        name = input( "Enter a name: " )
        source = input( "Enter a source: " )
        self.item = self.get_UA().create_item(name,source)
        if self._parent:
            self._parent.on_item_selected( self.item )
        return True

# select item
# when an item is selected, on_item_selected must be called
# TODO: create a SelectionSignleNode class to manage selection a single option
#       (handle with SelectionSingleNode.begin(), which returns the data)
class Selection_SelectItem(SelectionNode):
    def __init__( self, parent = None ):
        super().__init__( parent = parent, 
                          title = "Selecting Item",
                          access_prompt = "Select Item From Cart" )
        self.selected_item = None

    def _generate_children_nodes( self ):
        self.force_quit = False
        self.item_selections = self.get_UA().get_item_selections()
        
        if not self.item_selections:
            return list()

        children = list()
        for item_selection in self.item_selections:
            if not item_selection.read_access():
                continue # skip if no read access
            item = item_selection.get_item()
            item_appearance = f"{item.get_name()} from " + \
                              f"{item.get_source()[:20]}... " + \
                              f"(x{item_selection.get_quantity()})"
            selection_item = Selection_Item(item = item_selection.get_item(),
                                            item_appearance = item_appearance,
                                            parent = self)
            children.append(selection_item)

        return children

    def on_item_selected( self, selected_item ):
        self.selected_item = selected_item
        if self._parent:
            self._parent.on_item_selected( self.selected_item )
            self.force_quit = True

    def get_item_selected( self ):
        return self.selected_item
    

# representation of item as selection
class Selection_Item(SelectionNode):
    def __init__( self, item, item_appearance = "ITEM_APPEARANCE", parent = None ):
        self.item = item
        super().__init__( parent = parent, 
                          access_prompt = item_appearance,
                          title = "Item" )

    def begin( self ):
        if self._parent:
            self._parent.on_item_selected( self.item )
        return True






if __name__ == "__main__":
    try:
        selection_obj = Selection_LoginMenu()
        selection_obj.begin()
        print( "Program End Success" )
    except Exception as e:
        print( f"An Unexpected Error Occurred: {e}" )

    while True:
        input()






