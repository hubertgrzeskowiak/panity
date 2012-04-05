from panity.component import Component

class DummyComponent(Component):
    def __init__(self, game_object):
        Component.__init__(self, game_object)
        print "dummy component initialized in game object '{}'".format(
                                                                    game_object)
