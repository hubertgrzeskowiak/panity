from panity.component import Component
from panity.properties import PathProperty
from panda3d.core import NodePath

class Mesh(Component):

    path = PathProperty("")

    def __init__(self, game_object):
        Component.__init__(self, game_object)
        Mesh.path.addListener(self, self.reloadModel)
        self.model = None

    def reloadModel(self, path):
        if path == "" and self.model is not None:
                self.model.removeNode()
                self.model = None
        else:
            try:
                self.model = loader.loadModel(path)
            except NameError: # loader not available
                print "error. no loader"
            else:
                self.model.reparentTo(self.game_object.transform.node)

    def destroy(self):
        self.model.removeNode()

# Test
if __name__ == "__main__":
    m1 = Mesh(None)
    m2 = Mesh(None)
    assert m1.path == ""
    assert m2.path == ""
    m1.path = "m1 path"
    assert m1.path == "m1 path"
    assert m2.path == ""
    m2.path = "m2 path"
    assert m1.path == "m1 path"
    assert m2.path == "m2 path"