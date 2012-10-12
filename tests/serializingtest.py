from panity.gameobject import GameObject
from panity.component import Component
from panity.properties import *
from panity.xmlparser import *


go = GameObject("my new game object")
go.transform.local_position = [1.5, 5, 5]
mesh = go.addComponent("Mesh")
mesh.path = "smiley"
xml = getXMLFromGameObject(go)
print prettifyXML(xml)

new_go = getGameObjectFromXML(xml)
new_xml = getXMLFromGameObject(new_go)
print prettifyXML(new_xml)    
