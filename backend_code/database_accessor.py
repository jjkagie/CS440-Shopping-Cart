import backend_code.connection as connection
#try:
#    import config
#except ModuleNotFoundError:
#    raise ModuleNotFoundError(
#        """database information must be inserted into config_template, and renamed to config.py""")

class Config(object):
    HOST = '7a6.h.filess.io'
    DATABASE = 'CS440ShoppingCart_industrial'
    USER = 'CS440ShoppingCart_industrial'
    PASSWORD = 'a42ff5253a411662e184a51da2693e7bdf6c93a1'
    PORT = 3307

    CHARSET = 'utf8'
    UNICODE = True
    WARNINGS = True

    @classmethod
    def dbinfo(cls):
        return {
            'host': cls.HOST,
            'database': cls.DATABASE,
            'user': cls.USER,
            'password': cls.PASSWORD,
            'charset': cls.CHARSET,
            'use_unicode': cls.UNICODE,
            'get_warnings': cls.WARNINGS,
            'port': cls.PORT,
        }

# DatabaseAccessor
########### Use Cases
# run sql commmands

# run_select:
#   run command without modifying database
#   arguments:
#       sql_command - sql command string, with '%s' representing variables
#       argv - values to replace '%s's in sql_command
#   return:
#       list of tuples of requested attributes from command
#   ex: run_select( "SELECT cost FROM Houses WHERE loc=%s AND age<%s", "arizona", 10 )
#           runs "SELECT cost,age FROM Houses WHERE loc=arizona AND age<10"
#              and returns [("500","5"),("450","2"),("900","9"),("50","1")]

# run_change:
#   run command and modify the database
#   arguments: <same as run_select>
#   return:
#       False if unable to run command
#       otherwise, number of rows affected
#   ex: run_change( "INSERT INTO Houses VALUES(%s,%s,%s,%s)", "Blue", "arizona", 25, 215 )
#           runs "INSERT INTO Houses VALUES(Blue,arizona,25,215)"

# pause:
#   temporarily pauses the connection to the database
class DatabaseAccessor:
    def __init__( self ):
        self._config = Config().dbinfo()
        self._connection = connection.Connection( self._config )

    # ERROR: 0 is interpreted as False
    def run_select( self, sql_command, *argv ):
        try:
            if False in argv or None in argv:
                return False
            sql_args = tuple([str(arg) for arg in argv])
            return self._connection.run_select( sql_command, sql_args )
        except:
            return False

    # ERROR: 0 is interpreted as False
    def run_change( self, sql_command, *argv ):
        try:
            if False in argv or None in argv:
                return False
            sql_args = tuple([str(arg) for arg in argv])
            return self._connection.run_change( sql_command, sql_args )
        except:
            return False

    def pause( self ):
        return self._connection.pause()
    

database_accessor = DatabaseAccessor()



