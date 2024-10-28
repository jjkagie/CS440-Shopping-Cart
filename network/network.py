from message.message import Message
from connection.connection import connector
import pdb




class NetworkNode_Super:
    def __init__( self ):
        raise NotImplementedError
    
    def needs_node( self ):
        raise NotImplementedError

    def on_network_node_checked_out(self, provided_node):
        raise NotImplementedError

    def request_available_node(self, requester, min_bound = 0, max_bound = None):
        raise NotImplementedError

    def is_available(self):
        raise NotImplementedError

    def prepare_size_increase( self, num_bits = None ):
        raise NotImplementedError

    def publish_size_increase( self, num_bits = None ):
        raise NotImplementedError
    
    def connect_into_network(self, node_to_connect):
        raise NotImplementedError
    
    def print_connections(self):
        raise NotImplementedError

    def get_id(self):
        raise NotImplementedError

    def receive_message( self, message ):
        match message.type:
            case Message.request_available_node:
                return self.request_available_node( **(message.args) )
            case Message.on_network_node_checked_out:
                return self.on_network_node_checked_out( **(message.args) )
            case Message.needs_node:
                return self.needs_node( **(message.args) )
            case Message.is_available:
                return self.is_available( **(message.args) )
            case Message.connect_into_network:
                return self.connect_into_network( **(message.args) )
            case Message.print_connections:
                return self.print_connections( **(message.args) )
            case Message.change_node_info:
                return self.change_node_info( **(message.args) )
            case Message.prepare_size_increase:
                return self.prepare_size_increase( **(message.args) )
            case Message.publish_size_increase:
                return self.publish_size_increase( **(message.args) )
            case Message.get_network_node:
                return self.get_network_node( **(message.args) )
            case Message.get_id:
                return self.get_id( **(message.args) )
            
            case _:
                raise NotImplementedError("Message type {message.type} not recognized")
        return





class NetworkNode(NetworkNode_Super):
    def __init__( self, application=None, connection_info=None, node_id = 0,
                  network_bit_size = 0, is_available = False ):
        self.id = node_id
        self.connection_info = connection_info
        self.network_connections = list() # exponential connections
        self.network_bit_size = network_bit_size
        self.available = is_available
        self.application = application
        self.requesting_node = False
        self.is_prepared = False

    def is_available( self ):
        return self.available

    def needs_node( self ):
        return self.requesting_node

    def get_username( self ):
        return None

    def get_id( self ):
        return self.id

    # self: node already in network
    # requester: NetworkNode requesting the available node
    # recursively finds the lowest availble id in self's network
    # verifies that the requester still needs the node
    # mark the node as unavailable
    # notifies requester that the node was checked out
    def request_available_node(self, requester, min_bound = 0, max_bound = None):
        # identify bounds
        min_bound = max(min_bound, self.id + 1)
        if max_bound == None:
            max_bound = 2 ** self.network_bit_size - 1
        
        # recursively find lowest available id
        if not self.available:
            # binary search:
            #   middle value will be the largest available id
            #   if the middle value is avaiable:
            #       the least avaiable is before the middle value
            #       -> search between current and middle value (inclusive)
            #   if the middle value is unavailable:
            #       the least available is after the middle value
            #       -> search between middle value and max_bound
            search_nodes = [node for node in self.network_connections \
                            if node.id >= min_bound and node.id <= max_bound]

            for node in reversed(search_nodes):
                if node.is_available():
                    # available is below middle, continue searching downwards
                    max_bound = node.id
                else:
                    # available is above middle, search upwards
                    return node.request_available_node(requester, min_bound, max_bound)

            # at this point, every node that self is connected to is available
            # therefore, the smallest available node is the smallest node
            return search_nodes[0].request_available_node(requester,min_bound, max_bound)

        # verifies that the requester still needs the node
        if requester.needs_node():
            # mark the node as unavailable
            self.available = False

            # remove self from appplication
            self.application.unhandle_node(self)

            # notifies requester that the node was checked out
            return requester.on_network_node_checked_out(provided_node = self)
            
    def on_network_node_checked_out( self, **args ):
        return self.application.on_network_node_checked_out( **args )

    def prepare_size_increase(self):
        # exit if already implemented
        if self.is_prepared:
            return
        self.is_prepared = True

        # notify all nodes to prepare for size increase        
        for node in self.network_connections:
            node.prepare_size_increase()

        # double size
        prepared_bit_size = self.network_bit_size + 1
        prepared_size = 2 ** prepared_bit_size
        self.prepared_bit_size = prepared_bit_size

            # handle opposing node
        # create opposing node with same data
        node_id = self.id + ( prepared_size >> 1 )
        new_node = NetworkNode(application = self.application,
                               connection_info = self.connection_info,
                               node_id=node_id,
                               network_bit_size = prepared_bit_size,
                               is_available = True)
        # prepare to notify application to handle the new node
        self.prepared_new_node = new_node

        # generate prepared connections for self
        self.prepared_network_connections = list()
        for node_connect_number in range( prepared_bit_size ):
            node_id = ( self.id + 2 ** node_connect_number ) % prepared_size
            node_handler_id = node_id % ( prepared_size >> 1 )
            node_info = self.get_network_node(node_handler_id).connection_info
            node = NetworkNodeReference( node_info, node_id )
            self.prepared_network_connections.append( node )

        # generate prepared connections for prepared new node
        self.prepared_new_node_connections = list()
        for node_connect_number in range( prepared_bit_size ):
            node_id = ( self.prepared_new_node.id + 2 ** node_connect_number ) % prepared_size
            node_handler_id = node_id % ( prepared_size >> 1 )
            node_info = self.get_network_node(node_handler_id).connection_info
            node = NetworkNodeReference( node_info, node_id )
            self.prepared_new_node_connections.append( node )

    def publish_size_increase( self ):
        # skip if not prepared
        if not self.is_prepared:
            return
        self.is_prepared = False

        # publish increase for all nodes
        for node in self.network_connections:
            node.publish_size_increase()
        
        # update self's data
        self.network_bit_size = self.prepared_bit_size
        self.network_connections = self.prepared_network_connections

        # update prepared node's connection
        self.prepared_new_node.network_connections = self.prepared_new_node_connections

        # request prepared node to be handled
        self.application.handle_node( self.prepared_new_node )

    def get_network_node(self, node_id):
        network_size = 2**self.network_bit_size
        # return reference to self if meets requirements
        if node_id % network_size == self.id:
            return NetworkNodeReference(self.connection_info, self.id)

        target_id = node_id + network_size
        closest_node = self.network_connections[0]
        closest_distance = ( target_id - closest_node.id ) % network_size
        for test_node in self.network_connections:
            test_distance = ( target_id - test_node.id ) % network_size
            if test_distance < closest_distance:
                closest_distnace = test_distance
                closest_node = test_node
        return closest_node.get_network_node(node_id)

    

    def connect_into_network(self, node_to_connect):
        self.network_connections.append(node_to_connect)
        
    def print_connections(self):
        print( f"Connections for node {self.id} (controlled by " + \
               f"{self.application._Application__main_node.connection_info.ip}):" )
        for node in self.network_connections:
            print( f"  {node.id}" )
        print()

    # NOTE: cannot be done after shortcuts to self are created
    #       only intended for checking out a node
    def change_connection_info( self, connection_info ):
        # change self's info
        self.connection_info = connection_info
        # change everyone else's info
        # everyone else = (n-2**k)
        for i in range(self.network_bit_size):
            network_size = 2**self.network_bit_size
            connected_node_id = (self.id + network_size - 2 ** i)%network_size
            connected_node = self.get_network_node(connected_node_id)
            connected_node.change_node_info( node_id=self.id,
                                             connection_info=connection_info )

    def change_node_info( self, node_id, connection_info ):
        for node in self.network_connections:
            if node.id == node_id:
                node.connection_info = connection_info
        return


class NetworkNodeReference(NetworkNode_Super):
    def __init__( self, connection_info, node_id = None ):
        self.connection_info = connection_info
        self.id = node_id
    
    def get_id( self ):
        message = Message(Message.get_id,
                          sender = self.connection_info,
                          recipent = self.connection_info,
                          recipent_id = self.id )
        self.id = connector.send_message(message)
        return self.id

    def needs_node( self ):
        message = Message(Message.needs_node, 
                          sender = self.connection_info,
                          recipent = self.connection_info,
                          recipent_id = self.id )
        return connector.send_message(message)

    def on_network_node_checked_out(self, provided_node):
        message = Message(Message.on_network_node_checked_out,
                          sender = self.connection_info,
                          recipent = self.connection_info,
                          recipent_id = self.id, 
                            provided_node = provided_node)
        return connector.send_message(message)

    def request_available_node(self, requester, min_bound = 0, max_bound = None):
        message = Message(Message.request_available_node,
                          sender = self.connection_info,
                          recipent = self.connection_info,
                          recipent_id = self.id,
                          requester = requester,
                          min_bound = min_bound,
                          max_bound = max_bound )
        return connector.send_message(message)

    def is_available(self):
        message = Message(Message.is_available,
                                      sender = self.connection_info,
                                      recipent = self.connection_info,
                                      recipent_id = self.id)
        return connector.send_message(message)

    def prepare_size_increase( self ):
        message = Message(Message.prepare_size_increase,
                                      sender = self.connection_info,
                                      recipent = self.connection_info,
                                      recipent_id = self.id)
        return connector.send_message(message)

    def publish_size_increase( self ):
        message = Message(Message.publish_size_increase,
                                      sender = self.connection_info,
                                      recipent = self.connection_info,
                                      recipent_id = self.id)
        return connector.send_message(message)

    def connect_into_network(self, node_to_connect):
        message = Message(Message.connect_into_network,
                               sender = self.connection_info,
                               recipent = self.connection_info,
                              recipent_id = self.id, 
                               node_to_connect = node_to_connect)
        return connector.send_message(message)
    
    def print_connections(self):
        message = Message(Message.print_connections,
                               sender = self.connection_info,
                               recipent = self.connection_info,
                               recipent_id = self.id)
        return connector.send_message(message)

    def change_node_info( self, node_id, connection_info ):
        message = Message(Message.change_node_info,
                               sender = self.connection_info,
                               recipent = self.connection_info,
                               recipent_id = self.id,
                          node_id = node_id,
                          connection_info = connection_info)
        return connector.send_message(message)

    def get_network_node( self, node_id):
        message = Message(Message.get_network_node,
                               sender = self.connection_info,
                               recipent = self.connection_info,
                               recipent_id = self.id,
                          node_id=node_id)
        return connector.send_message(message)





