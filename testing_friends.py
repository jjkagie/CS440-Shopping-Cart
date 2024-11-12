from Friends.DatabaseAccessor.DatabaseAccessor import database_accessor
from Friends.DAO.DAO import create_tables
from Friends.DAO.Friend import Account, Friendship, FriendRequest
from Friends.CustomerAccessor.CustomerAccessor import CustomerAccessor

if __name__ == "__main__":
    # unique ids for test customers
    id0 = 2000000000
    id1 = 2000000001
    id2 = 2000000002
    
    # database accessor tests
    test_DA = False
    if test_DA:
        print( "Check Able to run Select" )
        print(database_accessor.run_select("SELECT * FROM Account"))

        create_tables()

        print(database_accessor.run_change("INSERT INTO Friendship VALUES (%s,%s)",
                                           str(id0), str(id1)))
        print(database_accessor.run_select("SELECT * FROM Friendship"))
        print(database_accessor.run_change("DELETE FROM Friendship WHERE account1=%s AND account2=%s",
                                           str(id0), str(id1)))
        print(database_accessor.run_select("SELECT * FROM Friendship"))

    test_DAO = False
    if test_DAO:
        a0 = Account(id0)
        a1 = Account(id1)
        a0.create()
        a1.create()

        # send request from 0 to 1
        r1 = FriendRequest(id0,id1)
        r1.create()

        # view requests
        r0_sent = a0.get_sent_requests()
        assert len(r0_sent)==1
        r0_received = a0.get_received_requests()
        assert len(r0_received)==0
        r1_sent = a1.get_sent_requests()
        assert len(r1_sent)==0
        r1_received = a1.get_received_requests()
        assert len(r1_received)==1

        # accept request from a1
        request = r1_received[0]
        friendship = Friendship(request.requester,request.target)
        assert friendship.create() == True
        assert request.remove() == True

        # access friendship
        f0 = a0.get_friendships()[0]
        f1 = a1.get_friendships()[0]
        assert f0.account1 == str(id0)
        assert f1.account1 == str(id0)
        assert f0.account2 == str(id1)
        assert f1.account2 == str(id1)
        
        # remove friendship
        assert f0.remove() == True

    test_CA = True
    if test_CA:
        # create customer accessors for each customer - login
        c0 = CustomerAccessor()
        c1 = CustomerAccessor()
        c2 = CustomerAccessor()

        c0.login(id0)
        c1.login(id1)
        c2.login(id2)

        # c0 sends request to c1 - send_friend_request, get_sent_requests
        assert c0.send_friend_request(id1)
        assert len(c0.get_sent_requests()) == 1

        # c1 accepts request - accept_request, get_received_requests
        request = c1.get_received_requests()[0]
        assert c0.accept_request(request) == False
        assert c1.accept_request(request) == True
        assert len(c0.get_friendships()) == 1

        # reject request - reject_request
        assert c0.send_friend_request(id2) == True
        request = c2.get_received_requests()[0]
        assert c2.reject_request(request) == True
        
        # verify friends are correct - get_friendship
        assert bool(c0.get_friendship(id1)) == True
        assert bool(c0.get_friendship(id2)) == False
        assert bool(c1.get_friendship(id2)) == False
        
        # c0 or c1 deletes friendship - get_friendships, remove_friendship
        friendship = c0.get_friendship(id1)
        assert bool(c0.get_friendship(id2)) == False
        assert c2.remove_friendship(friendship) == False
        assert c0.remove_friendship(friendship) == True

        # verify all data was removed (will not work when project is launached)
        #assert len(database_accessor.run_select("SELECT * FROM Friendship"))==0
        #assert len(database_accessor.run_select("SELECT * FROM FriendRequest"))==0

# database_accessor.run_change("DELETE FROM FriendRequest WHERE requester=0")
# database_accessor.run_change("DELETE FROM Friendship WHERE account1=0")

