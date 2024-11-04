from message.message import Message
from network.network import NetworkNode, NetworkNodeReference
from connection.connection import connector
from backend_code.customer_accessor import customer_accessor
import pdb

class Application:
    def __init__( self, connection_info ):
        self.__main_node = NetworkNode(self, connection_info = connection_info)
        self.handled_nodes = list() # nodes that application is solely responsible for
        self.saved_nodes = list() # nodes that application saved (disregard for connection)
        self.ca = customer_accessor(self)
        self.account = None

    # self: node wanting to connect to network
    # connection_info: node already connected to network
    # requests reference to check out a node for self
    # on completion, on_network_node_checked_out is called
    # NOTE: only call one time per application
    def network_node_check_out(self, connection_info):
        node_reference = NetworkNodeReference(connection_info = connection_info)
        node_reference.get_id()
        self.__main_node.requesting_node = True
        node_reference.request_available_node(requester=self.__main_node)
        return True

    # provided_node is the node provided from network_node_check_out
    # provided_node will become self's main connection node
    # changes provided_node's connection info to match self
    def on_network_node_checked_out(self, provided_node):
        # TODO: modularize, change provided_node to pass as reference
        # save old node
        old_node = self.__main_node

        # override old data
        self.__main_node = provided_node
        self.__main_node.requesting_node = False

        # change new node to match old node's connection
        self.__main_node.application = self
        self.__main_node.change_connection_info(old_node.connection_info)

    # called when a message is received
    def receive_message(self, message):
        # first, check if sending to main_node (default)
        recipent_id = message.recipent_id
        if recipent_id == None or self.__main_node.id == recipent_id:
            return self.__main_node.receive_message(message)

        # if not main_node, send to a handled node
        for node in self.handled_nodes:
            if node.id == recipent_id:
                return node.receive_message(message)
        raise ValueError("Requested node that is not connected to app")

    # handle_node: start handling node
    def handle_node(self, node_to_handle):
        self.handled_nodes.append(node_to_handle)

    # unhandle_node: stop handling node
    def unhandle_node(self, node_to_unhandle):
        for node in self.handled_nodes:
            if node.id == node_to_unhandle.id:
                self.handled_nodes.remove(node)
                break
        return

    # print all connections in network (including unavailable)
    def print_connections(self):
        print( f"--------------------------------" )
        print( f"Printing connections for app {self.__main_node.connection_info.ip}" )
        for i in range(2**self.__main_node.network_bit_size):
            node = self.__main_node.get_network_node(i)
            node.print_connections()
        print()

    # size modificcation
    def prepare_size_increase( self ):
        self.__main_node.prepare_size_increase()
    def publish_size_increase( self ):
        self.__main_node.publish_size_increase()

    def increase_size( self ):
        self.prepare_size_increase()
        self.publish_size_increase()


