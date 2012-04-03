class Object(object):
    """Base class for all game objects and components."""
    @staticmethod
    def instantiate(original, position=None, rotation=None):
        raise NotImplementedError("object doesn't implement instantiate")
    
    @staticmethod
    def destroy(obj, t=0.0):
        # TODO
        pass
    
    @staticmethod
    def destroyImmediate(obj, allowDestroyingAssets=False):
        # TODO
        pass
    
    @staticmethod
    def findObjectsOfType(typ):
        # TODO
        pass

    @staticmethod
    def findObjectOfType(typ):
        # TODO
        pass
    
    @staticmethod
    def dontDestroyOnLoad(target):
        # TODO
        pass
        
    def __init__(self):
        self.hideFlags = None
    
    def getInstanceId(self):
        return id(self)
    
    def __str__(self):
        return self.name
    
    toString = __str__
    #__repr__ = __str__

    @property
    def name(self):
        return getattr(self, "_name", "")
    @name.setter
    def name(self, new_name):
        self._name = new_name
