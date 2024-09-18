import mysql.connector
import pdb

# Connection
########## Intended Use Cases:
# connect to SQL database

# open_connection, close_connection:
#   open/close the connection to the database
#   returns if the operation was successful
# commit_changes:
#   executes all changes that were made into the database
#   returns if commit was successful
# run_select:
#   run sql command without modifying the database's information
#   returns result in format list<tuple<str(atrribute)>> if successful
#       otherwise returns None
# run_change:
#   run sql command, then commit changes made to the database
#   return number of rows modified if successful
#       otherwise returns None

# NOTE: run_select and run_change will not attempt to 
#       execute the command if a connection is already open
class Connection:
    # config_dict contains the parameters for the mysql.connector.Connect()
    def __init__( self, config_dict ):
        self.__connection = None
        self.__cursor = None
        self.__config = config_dict
    
    def open_connection( self ):
        self.__connection = mysql.connector.connect(**self.__config)
        self.__cursor = self.__connection.cursor()
        return self.is_connected()

    def is_connected( self ):
        if self.__connection:
            return self.__connection.is_connected()
        return False

    def close_connection(self):
        self.__cursor.close()
        self.__connection.close()
        self.__cursor = None
        self.__connection = None
        return not self.is_connected()

    def get_cursor(self):
        return self.__cursor

    def commit_changes( self ):
        if self.is_connected():
            self.__connection.commit()
            return True
        return False

    def run_select(self, sql, values=None):
        results = None
        if not self.is_connected():
            self.open_connection()
            # after opening the connection, catch exceptions to ensure 
            #   the connection is closed (if one is, return None)
            try:
                cursor = self.get_cursor()
                cursor.execute(sql, values)
                results = cursor.fetchall()
            except:
                pass
            self.close_connection()
            
        return results

    def run_change(self, sql, values=None):
        result = None
        if not self.is_connected():
            self.open_connection()
            # after opening the connection, catch exceptions to ensure 
            #   the connection is closed (if one is, return None)
            try:
                cursor = self.get_cursor()
                cursor.execute(sql, values)
                self.commit_changes()
                result = cursor.rowcount
            except:
                pass
            self.close_connection()
            
        return result




    
