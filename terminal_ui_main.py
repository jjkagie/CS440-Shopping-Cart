from terminal_ui.terminal_ui import Selection_LoginMenu
from network.application import Application
from connection.connection import ConnectionInfo


from backend_code.DAO import accounts

if __name__ == "__main__":
    # initialize data
    connection_info = ConnectionInfo("IP1","PORT1")
    application = Application(connection_info)
    customer_accessor = application.ca
    
    try:
        selection_obj = Selection_LoginMenu(customer_accessor = customer_accessor)
        selection_obj.begin()
        print( "Program End Success" )
    except Exception as e:
        print( f"An Unexpected Error Occurred: {e}" )

    
    print("Program End")



