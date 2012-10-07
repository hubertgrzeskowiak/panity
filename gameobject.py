import types

from panda3d.core import NodePath

import components
from components.transform import Transform
from object import Object

class GameObject(Object):
    """Base class for all entities. Every game object has a transform component
    by default.
    """
    def __init__(self, name=None, components=[]):
        Object.__init__(self)
        self.name = name if name else "unnamed game object"
        self.components = {}
        self.transform = Transform(self)
        for component in components:
            self.addComponent(component)

    def getChildren(self):
        """Return a list of children as game objects."""
        # this requires self.__iter__
        return [c for c in self]

    def __iter__(self):
        for t in self.transform:
            yield t.game_object

    def addComponent(self, component):
        """component can be class name or class. Instances of components are
        not allowed. The newly added component object is returned.
        """
        if type(component) in types.StringTypes:
            if component in self.components:
                raise AttributeError("game object {} already has a {} "+\
                    "component".format(self.transform.name, str(component)))
            comp_module = __import__("components."+component.lower(), globals(), locals(), [None])
            comp_class = getattr(comp_module, component)
            comp_object = comp_class(self)
            self.components[component] = comp_object
        else:
            # it's a class
            comp_name = component.__name__
            if comp_name in self.components:
                raise AttributeError("game object {} already has a {} "+\
                    "component".format(self.transform.name, comp_name))
            comp_object = component()
            self.components[comp_name] = comp_object
        return comp_object

    def getComponent(self, component):
        if self.components.has_key(component):
            return self.components[component]