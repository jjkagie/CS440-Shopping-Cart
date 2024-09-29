import mysql.connector
import pdb

# Connection
########## Intended Use Cases:
# connect to SQL database

# open_connection, close_connection:
#   open/close the connection to the database
#   returns if the connection is opened/closed
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
# pause:
#   disconnects from the database temporarily
class Connection:
    # config_dict contains the parameters for the mysql.connector.connect()
    def __init__( self, config_dict ):
        self.__connection = None
        self.__cursor = None
        self.__config = config_dict
    
    def open_connection( self ):
        if self.is_connected():
            return True
        try:
            self.__connection = mysql.connector.connect(**self.__config)
            self.__cursor = self.__connection.cursor()
            if self.__connection.is_connected():
                return True
        except:
            pass
        self.__connection = None
        self.__cursor = None
        return False

    def is_connected( self ):
        return self.__connection != None

    def close_connection(self):
        if not self.is_connected():
            return False
        try:
            self.__cursor.close()
            self.__connection.close()
            self.__cursor = None
            self.__connection = None
        except:
            pass
        return not self.is_connected()

    def get_cursor(self):
        return self.__cursor

    def commit_changes( self ):
        if self.is_connected():
            self.__connection.commit()
            return True
        return False

    def run_select(self, sql, values=None):
        self.open_connection()
        try:
            cursor = self.get_cursor()
            cursor.execute(sql, values)
            return cursor.fetchall()
        except:
            return None

    def run_change(self, sql, values=None):
        self.open_connection()
        try:
            cursor = self.get_cursor()
            cursor.execute(sql, values)
            self.commit_changes()
            return cursor.rowcount
        except:
            return None

    def pause( self ):
        return self.close_connection()

    # close connection when self is destructed
    def __del__( self ):
        self.close_connection()

