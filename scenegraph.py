class SceneGraph(object):
    def __init__(self):
        self.render = NodePath("render")
        self.render2d = NodePath("render2d")
        self.render2d.reparentTo(self.render)
        # set some transforms on render2d
        # ...
