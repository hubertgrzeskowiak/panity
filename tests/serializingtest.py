from panity.gameobject import GameObject
from panity.component import Component
from panity.properties import *
from panity.xmlsceneparser import *


go = GameObject()
go.addComponent("Mesh")
xml = getXMLFromGameObject(go)
print prettifyXML(xml)

new_go = getGameObjectFromXML(xml)
new_xml = getXMLFromGameObject(new_go)
print prettifyXML(new_xml)    