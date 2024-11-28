import pdb

# converts to format accepted by flask.jsonify
#  - dictionary where all values are strings or jsonifiables
class Jsonable(dict):
    def __init__( self, *args, **kwargs ):
        pdb.set_trace()
        for key,value in kwargs:
            if isinstance(value, Jsonible):
                
            super()[key] = str(value)





        
        if args:
            for arg in args:
                if isinstance(arg, Jsonible):
                    pass

                    


if __name__ == "__main__":
    print(Jsonible(my_val = 2, other_val = "Hello, World!"))




