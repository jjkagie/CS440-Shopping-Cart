import pdb

# converts to format accepted by flask.jsonify
#  - dictionary where all values are strings or jsonifiables
# NOTE: key 'other' is reserved for non-kwargs
# inherits from dict to allow jsonify access to any information it needs
class Jsonable(dict):
    def __init__( self, *argv, **kwargs ):
        # keyword arguments - set each value to their own key
        for key,value in kwargs.items():
            self[key] = Jsonable.to_jsonable_value(value)

        if argv:
            self["other"] = str([Jsonable.to_jsonable_value(arg) for arg in argv])

    # converts an object into an acceptable value for a jsonable object
    def to_jsonable_value(object_val):
        # Jsonable object -> keep format
        if isinstance(object_val,Jsonable):
            return object_val
        # not Jsonable object -> force to string
        return str(object_val)


if __name__ == "__main__":
    print(Jsonable(my_val = 2, other_val = "Hello, World!"))

    json_child1 = Jsonable(hello=1, world=2)
    json_child2 = Jsonable(hello=[1,2,3], world={3,4})
    json_parent = Jsonable(child1 = json_child1, child2 = json_child2,
                           value = 42)
    print(json_parent)

    print(Jsonable(2,"hello world", my_kwarg=42))





    
