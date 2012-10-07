class Root(object):
    """Pass this class the "render" nodepath and use the instance
    as parent attribute for new game objects.
    """
    def __init__(self, render):
        self.node = render