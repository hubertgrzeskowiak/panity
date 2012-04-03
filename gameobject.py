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
        self.__components = {}
        self.transform = Transform(self)
        for component in components:
            self.addComponent(component)    

    def __iter__(self):
        for t in self.transform:
            yield t.gameobject

    def addComponent(self, component):
        """component can be class name or class. Instances of components are
        not allowed. The newly added component object is returned.
        """
        if component in self.__components:
            raise AttributeError("game object {} already has a {} "+\
                "component".format(self.transform.name, str(component)))
        if type(component) in types.StringTypes:
            comp_module = getattr(components, component.lower())
            comp_class = getattr(comp_module, component)
            comp_object = comp_class(self)
            self.__components[component] = comp_object
        else:
            comp_object = component()
            self.__components.append(comp_object)
        return comp_object

    def getComponent(self, component):
        if self.__components.hasKey(component):
            return self.__components[component]

    @property
    def transform(self):
        return self._transform
    @transform.setter
    def transform(self, transform):
        """transform is an instance of the Transform component.
        This copies all properties of the passed transforms onto the current one.
        """
        if getattr(self, "_transform", None):
            self._transform._destroy()
        self._transform = transform
        self.__components["transform"] = transform
