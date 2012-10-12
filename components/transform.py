from panda3d.core import NodePath

from panity.component import Component
from panity.properties import SerializedPropertyDecorator

class Transform(Component):
    """Each game object has exactly one of these. A transform holds data
    about position, rotation, scale and parent relationship.
    
    In Panity this is a wrapper for a NodePath.
    """

    def __init__(self, game_object, name):
        # Component class sets self.game_object = game_object
        Component.__init__(self, game_object)
        self.node = NodePath(name)
        self.node.setPythonTag("transform", self)

    @classmethod
    def getClassSerializedProperties(cls):
        """Return all special property attributes in a dict. Only attributes
        derived from SerializedProperty are respected.

        On transform component this method always returns local position,
        -rotation and scale only.
        """
        d = {}
        d["local_position"] = Transform.local_position
        d["local_euler_angles"] = Transform.local_euler_angles
        d["local_scale"] = Transform.local_scale
        return d

    def getSerializedProperties(self):
        """Return all properties for serialization. In the case of transform
        this only returns local position, -rotation and -scale, which are
        required to restore the state of the node.
        """
        d = {}
        d["local_position"] = self.local_position
        d["local_euler_angles"] = self.local_euler_angles
        d["local_scale"] = self.local_scale
        return d

    # We use the panda node to save the name on it for better debugging and
    # efficient finding of nodes with NodePath().find()
    @SerializedPropertyDecorator
    def name(self):
        return self.node.getName()
    @name.setter
    def name(self, name):
        if name == "render":
            name = "_render"
        self.node.setName(name)

    @SerializedPropertyDecorator
    def position(self):
        return self.node.getPos(self.root.node)
    @position.setter
    def position(self, position):
        self.node.setPos(self.root.node, *position)
    
    @SerializedPropertyDecorator
    def local_position(self):
        return self.node.getPos()
    @local_position.setter
    def local_position(self, position):
        self.node.setPos(*position)

    @SerializedPropertyDecorator
    def euler_angles(self):
        return self.node.getHpr(self.root.node)
    @euler_angles.setter
    def euler_angles(self, angles):
        self.node.setHpr(self.root.node, *angles)
    
    @SerializedPropertyDecorator
    def local_euler_angles(self):
        return self.node.getHpr()
    @local_euler_angles.setter
    def local_euler_angles(self, angles):
        self.node.setHpr(*angles)
    
    @SerializedPropertyDecorator
    def rotation(self):
        return self.node.getQuat(self.root.node)
    @rotation.setter
    def rotation(self, quaternion):
        self.node.setQuat(self.root.node, *quaternion)

    @SerializedPropertyDecorator
    def local_rotation(self):
        return self.node.getQuat()
    @local_rotation.setter
    def local_rotation(self, quaternion):
        self.node.setQuat(*quaternion)

    @SerializedPropertyDecorator
    def local_scale(self):
        return self.node.getScale()
    @local_scale.setter
    def local_scale(self, scale):
        self.node.setScale(*scale)

    @SerializedPropertyDecorator
    def parent(self):
        p = self.node.getParent()
        if p.isEmpty() or p.getName() == "render":
            return self
        elif p.hasPythonTag("transform"):
            return p.getPythonTag("transform")
    @parent.setter
    def parent(self, parent):
        self.node.wrtReparentTo(parent.node)

    @SerializedPropertyDecorator
    def root(self):
        if self.parent is not self:
            return self.parent.root()
        else:
            return self
    
    def destroy(self):
        """Ultimately remove this transform. Warning: this might cause errors
        for other components on this game object.
        """
        self.node.removeNode()

    def getChildren(self):
        """Return children as Transforms."""
        # this requires the __iter__() method
        return [c for c in self]

    def __iter__(self):
        """Iterate over children nodes and yield the transform instances."""
        for child in self.node.getChildren():
            if child.hasPythonTag("transform"):
                yield child.getPythonTag("transform")
    
    def __str__(self):
        r = "Transform for '{}'\n".format(self.name)
        r += "local position: {}\n".format(self.local_position)
        r += "local rotation: {}\n".format(self.local_euler_angles)
        r += "local scale:    {}\n".format(self.local_scale)
        return r
