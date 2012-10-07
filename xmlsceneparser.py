try:
    from xml.etree import cElementTree as etree
except ImportError:
    from xml.etree import ElementTree as etree

import os.path
import pkgutil

from parserinterface import ParserInterface
from xmlvalidator import validateScene
from gameobject import GameObject
from component import Component
import components as components_package
import util

# Find out what components we have
_pkgpath = os.path.dirname(components_package.__file__)
COMPONENT_MODULES = [name for _, name, _ in pkgutil.iter_modules([_pkgpath])]

def prettifyXML(xml_code):
    """Pass it some xml in string and it will return a nicely formatted
    version. The content will stay exactly the same.
    """
    import xml.dom.minidom
    xml = xml.dom.minidom.parseString(xml_code)
    return xml.toprettyxml()


def getSceneFromXMLElement(element, root_name="scene", validate=True):
    root = GameObject(str(root_name))
    for xml_go in element:
        go = getGameObjectFromXML(xml_go)
        go.transform.parent = root.transform
    return root

def getSceneFromXMLFile(filename, validate=True):
    xml_scene = etree.parse(filename).getroot()
    root = filename.rsplit(".xml", 1)[0]
    return getSceneFromXMLElement(xml_scene, root, validate)

def getSceneFromXML(xml, root_name="scene", validate=True):
    return getSceneFromXMLElement(etree.fromstring(xml))

def getGameObjectFromXML(xml):
    """Create a game object from xml and append it as child of the parent
    game object. This function calls itself recursively. Prefabs are loaded
    using self.getGameObjectFromPrefab().
    The xml parameter can be either a string, in which case it will be
    parsed as xml or an etree.Element.
    """

    if isinstance(xml, str):
        xml = etree.fromstring(xml)

    # prefab means we should create an instance of a prefab and extend it
    prefab = xml.get("prefab")
    name = xml.get("name") or "unnamed"
    if prefab:
        go = getGameObjectFromPrefab(prefab, name)
    else:
        # prefab attribute not set. Use a new game object
        go = GameObject(name=name)
    for go_or_comp in xml:
        # a game object can contain game objects and components
        if go_or_comp.tag == "gameobject":
            xml_go = go_or_comp
            child = getGameObjectFromXML(xml_go)
            child.parent = go
        else: # must be a component otherwise
            xml_comp = go_or_comp
            # does the GO already have such a component?
            comp = go.getComponent(xml_comp.get(xml_comp.tag))
            if not comp:
                # if not, create it
                try:
                    comp = go.addComponent(xml_comp.tag)
                except ImportError, e:
                     print "".join(["Importing component {} failed! ",
                                   "Skipping."]).format(xml_comp.tag)
            else:
                print "".join(["second appearence of component '{}' ",
                               "in game object '{}' ignored"]).format(
                               xml_comp.tag, go.name)
            for option in xml_comp:
                setattr(comp, option, option.text)

    go.name = name
    return go

def getGameObjectFromPrefab(prefab_source, name):
    """Create a game object from a prefab, which corresponds to a
    prefab file from the prefabs package or something.
    """
    raise NotImplementedError
    # TODO:
    # import prefab
    # instantiate it
    # call Object.instantiate()
    # or
    # call PrefabUtility.getPrefabObject()

def getXMLFromScene(scene,):
    """Serialize a whole scene to xml code."""
    #xml = ""
    #xml += '<?xml version="1.0" encoding="UTF-8"?>'
    pass

def getXMLFromGameObject(game_object):
    xml = etree.Element("gameobject")
    xml.attrib["name"] = game_object.name
    for component in game_object.components.values():
        xml.append(etree.fromstring(getXMLFromComponent(component)))
    for child in game_object:
        xml.append(etree.fromstring(getXMLFromGameObject(child)))
    return etree.tostring(xml)

def getXMLFromComponent(component):
    name = type(component).__name__
    name = util.camelToSnake(name)
    xml = etree.Element(name)
    for p, v in component.getSerializedProperties().iteritems():
        child = etree.Element(util.camelToSnake(p))
        child.text = str(v)
        xml.append(child)
    return etree.tostring(xml)