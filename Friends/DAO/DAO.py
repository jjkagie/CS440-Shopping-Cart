from Friends.DatabaseAccessor.DatabaseAccessor import database_accessor

import pdb

# DAO (Database Access Object)
########## Intended Use Cases:
# create, update, load, and remove data from database


########## Keep information in DAO and Database up-to-date
# create:
#   adds DAO to the database
#       database:   primary keys    - set to keys in DAO
#                   values          - set to values in DAO
#       DAO:        primary keys    - must not exist in database
#                   values          - 

# load:
#   stores database values into DAO
#       database:   primary keys    - 
#                   values          - 
#       DAO:        primary keys    - must exist in database
#                   values          - set to values in database

# update:
#       database:   primary keys    - 
#                   values          - set to values in DAO
#       DAO:        primary keys    - must exist in database
#                   values          - must be non-null

# remove:
#       database:   primary keys    - removed
#                   values          - removed
#       DAO:        primary keys    - must exist in database
#                   values          -


########## modify/read information
# get_<key/value>: (requires read access)
#   returns the specified value from the DAO
# set_<value>: (requires write access)
#   changes the specified value in the DAO
#       NOTE: does not automatically update the database
class DAO:
    def __init__( self ):
        pass
    
    def create( self ):
        raise NotImplemented("Attempted to call abstract method")

    def update( self ):
        raise NotImplemented("Attempted to call abstract method")

    def remove( self ):
        raise NotImplemented("Attempted to call abstract method")

    def load( self ):
        raise NotImplemented("Attempted to call abstract method")



# creates all tables if they do not already exist
# does not change existing tables
def create_tables():
    database_accessor.run_change(
    """
    CREATE TABLE Friendship
            ( account1 int,
              account2 int,
              PRIMARY KEY(account1,account2)
            )
    """)


    database_accessor.run_change(
    """
    CREATE TABLE FriendRequest
            ( requester int,  
              target int,
              PRIMARY KEY(requester,target)
            )
    """)


    database_accessor.pause()





