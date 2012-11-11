try:
    from xml.etree import cElementTree as etree
except ImportError:
    from xml.etree import ElementTree as etree

import os.path
import pkgutil

from panda3d.core import VBase2, VBase3, VBase4

from parserinterface import ParserInterface
from xmlvalidator import validateScene
from gameobject import GameObject
from component import Component
import components as components_package
import util

# Find out what components we have
_pkgpath = os.path.dirname(components_package.__file__)
COMPONENT_MODULES = [name for _, name, _ in pkgutil.iter_modules([_pkgpath])]

# UTILITY STUFF

def prettifyXML(xml_code):
    """Pass it some xml in string and it will return a nicely formatted
    version. The content will stay exactly the same.
    """
    import xml.dom.minidom
    xml = xml.dom.minidom.parseString(xml_code)
    return xml.toprettyxml()


# SCENE

def getSceneFromXMLElement(element, root_name="scene", validate=True):
    root = GameObject(str(root_name))
    for xml_go in element:
        go = getGameObjectFromXMLElement(xml_go)
        go.transform.parent = root.transform
    return root

def getSceneFromXMLFile(filename, validate=True):
    xml_scene = etree.parse(filename).getroot()
    root = filename.rsplit(".xml", 1)[0]
    return getSceneFromXMLElement(xml_scene, root, validate)

def getSceneFromXML(xml_code, root_name="scene", validate=True):
    return getSceneFromXMLElement(etree.fromstring(xml_code))


def getXMLElementFromScene(scene):
    raise NotImplementedError 

def getXMLFromScene(scene):
    """Serialize a whole scene to xml code."""
    raise NotImplementedError


# GAME OBJECT

def getGameObjectFromXML(xml_code):
    xml_go = etree.fromstring(xml_code)
    return getGameObjectFromXMLElement(xml_go)

def getGameObjectFromXMLElement(element):
    # prefab means we should create an instance of a prefab and extend it
    prefab = element.get("prefab")
    name = element.get("name") or "unnamed game object"
    if prefab:
        go = getGameObjectFromPrefabFileName(prefab, name)
    else:
        # prefab attribute not set. Use a new game object
        go = GameObject(name)
    for go_or_comp in element:
        # a game object can contain game objects and components
        if go_or_comp.tag == "gameobject":
            xml_go = go_or_comp
            child = getGameObjectFromXMLElement(xml_go)
            child.parent = go
        else: # must be a component otherwise
            getComponentFromXMLElement(go_or_comp, go)
    return go

def getGameObjectFromPrefabFileName(filename):
    raise NotImplementedError


def getXMLElementFromGameObject(game_object):
    xml = etree.Element("gameobject")
    xml.attrib["name"] = game_object.name
    for component in game_object.components.values():
        xml.append(getXMLElementFromComponent(component))
    for child in game_object:
        xml.append(getXMLElementFromGameObject(child))
    return xml 

def getXMLFromGameObject(game_object):
    xml_element = getXMLElementFromGameObject(game_object)
    return etree.tostring(xml_element)


# COMPONENT

def getComponentFromXMLElement(element, game_object):
    # does the GO already have such a component?
    comp = game_object.getComponent(util.snakeToCamel(element.tag))
    if not comp:
        # if not, create it
        try:
            comp = game_object.addComponent(util.snakeToCamel(element.tag))
        except ImportError, e:
             print "".join(["Importing component {} failed! ",
                           "Skipping."]).format(element.tag)
             return


    for option in element:
        # check if it might be an array of numbers
        if option.text is None:
            continue
        str_nums = option.text.split(" ")
        try:
            nums = map(float, str_nums)
        except ValueError:
            # couldn't convert strings to numbers. it must be a str
            setattr(comp, option.tag, option.text)
        else:
            # conversion to a floats was successful, assign them as
            # list of floats
            setattr(comp, option.tag, nums)

def getXMLElementFromComponent(component):
    name = type(component).__name__
    name = util.camelToSnake(name)
    xml = etree.Element(name)
    for p, v in type(component).getClassSerializedProperties().iteritems():
        child = etree.Element(util.camelToSnake(p))
        child.text =  v.toXML(v.getValue(component))
        xml.append(child)
    return xml

def getXMLFromComponent(component):
    return etree.tostring(getXMLElementFromComponent(component))