from terminal_ui.terminal_ui import Selection_LoginMenu
from network.application import Application
from connection.connection import *


from backend_code.DAO import accounts

if __name__ == "__main__":
    # initialize applications
    connection_infos = [ConnectionInfo(f"IP{i}",f"PORT{i}") for i in range(16)]
    applications = [Application(connection_info) for connection_info in connection_infos]
    for connection_info,application in zip(connection_infos,applications):
        connector.add_connection(connection_info,application)

    # initialize data for main object
    i = 0
    while True:
        application = applications[i]
        customer_accessor = application.ca
        try:
            selection_obj = Selection_LoginMenu(customer_accessor = customer_accessor)
            selection_obj.begin()
            print( "Program End Success" )
            
        except Exception as e:
            print( f"An Unexpected Error Occurred: {e}" )

        print( "------------------------------------" )
        print( f"Moving to next application" )
        i += 1

    print("Program End")



