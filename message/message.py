

class Message:
    # message types:
    request_available_node = 0
    on_network_node_checked_out = 1
    needs_node = 2
    is_available = 3
    connect_into_network = 5
    print_connections = 6 # for testing
    change_node_info = 7
    prepare_size_increase = 8
    publish_size_increase = 9
    get_network_node = 10
    get_id = 11
    get_account = 12
    search_for_username = 13
    
    # message_type: Message.type
    # sender: connection_info
    # recipent: connection_info
    # recipent_id: network_node_id of recipent
    # **args: other arguments
    def __init__( self, message_type, sender, recipent, recipent_id, **args ):
        self.type = message_type
        self.sender = sender # incorrect information - this will always be application's info
        self.recipent = recipent
        self.recipent_id = recipent_id
        self.args = args

    def __str__( self ):
        return f"Message {self.type} to {self.recipent.ip}"




