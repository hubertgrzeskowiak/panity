from abc import ABCMeta, abstractmethod

class ParserInterface(object):
    """This interface shows what API a parser for scenes and prefabs should
    support at least.
    """
    __metaclass__ = ABCMeta
    
    #@staticmethod
    @abstractmethod
    def read(source):
        """Read a scene/prefab from source (file) and return a scene made out
        of game objects and components.
        """
        raise NotImplementedError

    #@staticmethod
    @abstractmethod
    def write(source, data):
        """Write a scene/prefab to a source (file)."""
        raise NotImplementedError
