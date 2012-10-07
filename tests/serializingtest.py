from panity.gameobject import GameObject
from panity.component import Component
from panity.properties import *
from panity.xmlsceneparser import *

class SomeComponent(Component):

    path = PathProperty()
    speed = FloatProperty()
    size = UnsignedIntegerProperty(1)

    def __init__(self):
        self.path = "/lol/whatever"
        self.speed = 123456.0


class SomeOtherComponent(Component):

    source = PathProperty()
    fun = FloatProperty(1337)
    size = UnsignedIntegerProperty(1)

    def __init__(self):
        self.source = "ummmm"


if __name__ == "__main__":
    go = GameObject()
    go.addComponent(SomeComponent)
    go.addComponent(SomeOtherComponent)
    print prettifyXML(getXMLFromGameObject(go))