import connection
import config


class DatabaseAccessor:
    def __init__( self ):
        self._config = config.Config().dbinfo()
        self._connection = connection.Connection( self._config )

    def run_change_depricated( self, sql_command, sql_args = tuple() ):
        return self._connection.run_change( sql_command, sql_args )

    def run_select( self, sql_command, *argv ):
        if False in argv or None in argv:
            return False
        sql_args = tuple([str(arg) for arg in argv])
        return self._connection.run_select( sql_command, sql_args )

    def run_change( self, sql_command, *argv ):
        if False in argv or None in argv:
            return False
        sql_args = tuple([str(arg) for arg in argv])
        return self._connection.run_change( sql_command, sql_args )


database_accessor = DatabaseAccessor()






