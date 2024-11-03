class Values:
    def __init__(self):
        self._values = dict()

class ID:
    def __init__(self, type="", keys=dict()):
        self._type = type
        self._keys = keys
    def GetHashIndex(self):
        return NotImplemented
