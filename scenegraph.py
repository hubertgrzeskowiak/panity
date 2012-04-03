class SceneGraph(object):

    global_instance = None

    def __init__(self):
        self.render = NodePath("render")
        self.render2d = NodePath("render2d")
        self.render2d.reparentTo(self.render)
        # set some transforms on render2d
        # ...
        # you should copy big parts of ShowBase here

    @staticmethod
    def getGlobalInstance():
        if not SceneGraph.global_instance:
            SceneGraph.global_instance = SceneGraph()
        return SceneGraph.global_instance
