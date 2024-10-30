import pdb

# https://stackoverflow.com/questions/6527633/how-can-i-make-a-deepcopy-of-a-function-in-python
# create copy of a function object
import types
def copy_function(f, name=None):
    '''
    return a function with same code, globals, defaults, closure, and 
    name (or provide a new name)
    '''
    fn = types.FunctionType(f.__code__, f.__globals__, name or f.__name__,
        f.__defaults__, f.__closure__)
    # in case f was given attrs (note this dict is a shallow copy):
    fn.__dict__.update(f.__dict__)
    return fn

class Broker(object):
    def __init__( self ):
        self.__initialize_attributes(self.get_handled_messages())
        self.__subscriptions = dict()

    # on_... will be called every time the publisher calls publish_...
    def subscribe( self, subscriber, publisher):
        self.__subscriptions.setdefault(publisher, list())
        self.__subscriptions[ publisher ].append( subscriber )

    # calls on_... for every subscriber subscribed to the publisher
    def __publish_message(self, publisher, handled_message = None, **kwargs):
        self.__subscriptions.setdefault(publisher, list())
        for subscriber in self.__subscriptions[publisher]:
            getattr(subscriber, "on_"+handled_message)(**kwargs)

    # initialize publish_... methods
    def __initialize_attributes(self, handled_messages):
        for handled_message in handled_messages:
            name = "publish_"+handled_message
            publish_message_copy = copy_function( self.__publish_message, name=name )
            # TODO: find a way to do this without pre-setting the default
            publish_message_copy.__defaults__ = (handled_message,)
            setattr(type(self), name, publish_message_copy)

    # abstact method
    # return list of strings of every action the broker can distribute
    def get_handled_messages( self ):
        raise NotImplementedError

# CustomerAccessor Broker
class Broker_CA(Broker):
    def get_handled_messages( self ):
        return "create_account", "login", "view_account", \
               "add_item_to_cart", "remove_item_from_cart", \
               "get_item_selections", "delete_account", \
               "create_item", "view_item_selections"

broker_ca = Broker_CA()
try:
    broker_dao = Broker_DAO()
except e:
    raise NotImplementedError("Broker_DAO was not implemented")

if __name__ == "__main__":
    class Subscriber:
        def __init__( self, value ):
            self.value = value
        def __str__( self ):
            return "Subscriber"+str( self.value )
        def on_create_account(self, account, value):
            print( f"{self} received on_create_account: {account,value}" )
        def on_login(self, success = True):
            print( f"{self} received on_login: {success}" )
    class Publisher:
        def __init__( self, value ):
            self.value = value
        def __str__( self ):
            return "Publisher"+str( self.value )
    
    publisher1 = Publisher(1)
    publisher2 = Publisher(2)
    subscriber1 = Subscriber(1)
    subscriber2 = Subscriber(2)

    broker_ca.subscribe(subscriber1, publisher1)
    broker_ca.subscribe(subscriber2, publisher1)
    broker_ca.subscribe(subscriber1, publisher2)

    print( f"\n{publisher1} published create account" )
    broker_ca.publish_create_account(publisher=publisher1, account="my_account", value=2)
    print( f"\n{publisher1} published login" )
    broker_ca.publish_login(publisher=publisher1, success=True)

    print( f"\n{publisher2} published login" )
    broker_ca.publish_login(publisher=publisher2, success=False)





