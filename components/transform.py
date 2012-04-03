from panity.component import Component
from panda3d.core import NodePath

class Transform(Component):
    """Each game object has exactly one of these. A transform holds data
    about position, rotation, scale but also parent and child relationships.
    
    In Panity this is a wrapper for a NodePath.
    """
    def __init__(self, game_object):
        # Component class sets self.game_object = game_object
        Component.__init__(self, game_object)
        self.node = NodePath(game_object.name)
        self.node.setPythonTag("transform", self)
        self.root = self

    # We use the panda node to save the name on it for better debugging and
    # efficient finding of nodes with NodePath().find()
    @property
    def name(self):
        return self.node.getName()
    @name.setter
    def name(self, name):
        self.node.setName(name)

    @property
    def position(self):
        return self.node.getPos(self.root.node)
    @position.setter
    def position(self, position):
        self.node.setPos(self.root.node, position)
    
    @property
    def local_position(self):
        return self.node.getPos()
    @local_position.setter
    def local_position(self, position):
        self.node.setPos(position)

    @property
    def euler_angles(self):
        return self.node.getHpr(self.root.node)
    @euler_angles.setter
    def euler_angles(self, angles):
        self.node.setHpr(self.root.node, angles)
    
    @property
    def local_euler_angles(self):
        return self.node.getHpr()
    @local_euler_angles.setter
    def local_euler_angles(self, angles):
        self.node.setHpr(angles)
    
    @property
    def rotation(self):
        return self.node.getQuat(self.root.node)
    @rotation.setter
    def rotation(self, quaternion):
        self.node.setQuat(self.root.node, quaternion)

    @property
    def local_rotation(self):
        return self.node.getQuat()
    @local_rotation.setter
    def local_rotation(self, quaternion):
        self.node.setQuat(quaternion)

    @property
    def local_scale(self):
        return self.node.getScale()
    @local_scale.setter
    def local_scale(self, scale):
        self.node.setScale(scale)

    @property
    def parent(self):
        return self.node.getParent()
    @parent.setter
    def parent(self, parent):
        self.node.wrtReparentTo(parent.node)
    
    def destroy(self):
        """Ultimately remove this transform. Warning: this might cause errors
        for other components on this game object.
        """
        self.node.removeNode()

    def getChildren(self):
        """Return children as Transforms."""
        # this requires the following method __iter__
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
