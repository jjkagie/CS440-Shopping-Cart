from message.message import Message


class ConnectionInfo:
    # ip/port are used to uniquely identify an application
    def __init__( self, ip, port ):
        self.ip = ip
        self.port = port

    # hash/eq used to index ConnectionInfo
    #   ConnectionInfo objects with the same ip and port will be consider equal
    def __hash__( self ):
        return hash((self.ip,self.port))
    def __eq__( self, other ):
        if not isinstance( other, ConnectionInfo ):
            return False
        return self.ip == other.ip and self.port == other.port




class Connector:
    # sends a message to message.recipent
    # message.recipent.ip and message.recipent.port
    #   are the recipent's ip and port
    # send message to Application by callling Application.receive_message(message)
    def send_message( self, message ):
        raise NotImplementedError()



# mock connector class for testing
class Connector_MOCK(Connector):
    # 
    def __init__( self ):
        self.__connections = dict()

    def send_message( self, message ):
        return self.__connection[ message.recipent ].receive_message(message)

    # explicitly create a way to connect to an IP and PORT.
    #   (this should not be necessary for the peer-to-peer system)
    def add_connection( self, connection_info, application ):
        self.__connection[ connection_info ] = application


# change to "connector = Connector()"
connector = Connector_MOCK()



