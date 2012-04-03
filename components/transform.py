from component import Component
from panda3d.core import NodePath

class Position(object):
    def __set__(self, instance, value):
        pass
        # TODO
    def __get__(self, instance, owner):
        print instance.__node


class Transform(Component):

    def __init__(self, gameobject):
        Component.__init__(self, gameobject)
        self.__node = NodePath(gameobject.name)
        self.__node.setPythonTag("transform", self)
        self.root = self

    # We use the panda node to save the name on it for better debugging and
    # efficient finding of nodes with NodePath().find()
    @property
    def name(self):
        return self.__node.getName()
    @name.setter
    def name(self, name):
        self.__node.setName(name)

    position = Position()
    #@property
    #def position(self):
    #    return self.__node.getPos(self.root.__node)
    #@position.setter
    #def position(self, position):
    #    self.__node.setPos(self.root.__node, position)
    
    @property
    def local_position(self):
        return self.__node.getPos()
    @local_position.setter
    def local_position(self, position):
        self.__node.setPos(position)

    @property
    def euler_angles(self):
        return self.__node.getHpr(self.root.__node)
    @euler_angles.setter
    def euler_angles(self, angles):
        self.__node.setHpr(self.root.__node, angles)
    
    @property
    def local_euler_angles(self):
        return self.__node.getHpr()
    @local_euler_angles.setter
    def local_euler_angles(self, angles):
        self.__node.setHpr(angles)
    
    @property
    def rotation(self):
        return self.__node.getQuat(self.root.__node)
    @rotation.setter
    def rotation(self, quaternion):
        self.__node.setQuat(self.root.__node, quaternion)

    @property
    def local_rotation(self):
        return self.__node.getQuat()
    @local_rotation.setter
    def local_rotation(self, quaternion):
        self.__node.setQuat(quaternion)

    @property
    def local_scale(self):
        return self.__node.getScale()
    @local_scale.setter
    def local_scale(self, scale):
        self.__node.setScale(scale)

    @property
    def parent(self):
        return self.__node.getParent()
    @parent.setter
    def parent(self, parent):
        print "meow"
        self.__node.wrtReparentTo(parent.__node)
    
    def _destroy(self):
        """Ultimately remove this transform. Warning: this might cause errors
        for other components on this game object.
        """
        self.__node.removeNode()
    
    def children(self):
        return self.__node.getChildren()
    
    def __iter__(self):
        """Iterate over children nodes and yield the transform instances."""
        for child in self.__node.getChildren():
            if child.hasPythonTag("transform"):
                yield child.getPythonTag("transform")
    
    def __str__(self):
        r = "Transform for '{}'\n".format(self.name)
        r += "local position: {}\n".format(self.local_position)
        r += "local rotation: {}\n".format(self.local_euler_angles)
        r += "local scale:    {}\n".format(self.local_scale)
        return r
