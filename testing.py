from message.message import Message
from network.network import NetworkNode
from network.application import Application
from connection.connection import ConnectionInfo, connector
from backend_code.customer_accessor import customer_accessor

# testing connections
# initialize connection information and applications
    # (when using ips and ports, connector will not require add_connection)
app_infos = [ConnectionInfo(f"IP{i}",f"Port{i}") for i in range(20)]
apps = [Application(app_info) for app_info in app_infos]
[connector.add_connection(app_info,app) for app_info,app in zip(app_infos,apps)]



# double network size for app0 twice (x4 nodes)
apps[0].increase_size()
apps[0].increase_size()


# have 3 external apps check out a node from app0
apps[1].network_node_check_out(app_infos[0])
apps[2].network_node_check_out(app_infos[0])
apps[3].network_node_check_out(app_infos[0])


# app0's network is full -> double again (x8 nodes)
#   (because app0 and app3 share networks, both have control over size)
apps[3].increase_size()

# check out more nodes using any app_info in the existing network
apps[4].network_node_check_out(app_infos[1])
apps[5].network_node_check_out(app_infos[0])
apps[15].network_node_check_out(app_infos[4])

# display final values
    # shows each node in app0's network
apps[0].print_connections()




# testing useraccessor
try:
    apps[0].ca.create_account("Michael", "my_password")
except Exception as e:
    pass
apps[0].ca.login("Michael", "my_password")
chair_item = apps[0].ca.create_item("chair","chairs.com")
apps[0].ca.add_item_to_cart(chair_item, 5)

desk_item = apps[0].ca.create_item("desk","desks.com")
apps[0].ca.add_item_to_cart(desk_item, 10)
large_desk_item = apps[0].ca.create_item("desk 2","big_desks.com")
apps[0].ca.add_item_to_cart(large_desk_item, 1)

apps[0].ca.view_item_selections()

apps[0].ca.remove_item_from_cart(desk_item)

apps[0].ca.view_item_selections()

apps[0].ca.delete_account()












