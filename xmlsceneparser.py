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

# Find out what components we have
_pkgpath = os.path.dirname(components_package.__file__)
COMPONENT_MODULES = [name for _, name, _ in pkgutil.iter_modules([_pkgpath])]


class XMLSceneParser(ParserInterface):
    """An xml parser for scenes."""
    @staticmethod
    def getSceneFromXML(xml, validate=True):
        """Read a scene from xml code or an xml file (xml argument ends
        with '.xml'), create it and return a root game object.
        AssertionErrors can be thrown when validation fails.
        """
        # TODO: get the path from vfs and os-specific (appropriate for etree)

        if xml.endswith(".xml"):
            xmlscene = etree.parse(xml)
            root = GameObject(xml.rsplit(".xml", 1)[0])
        else:
            xmlscene = etree.fromstring(xml)
            root = GameObject("scene")

        if validate:
            validateScene(xmlscene.getroot())

        for xml_go in xmlscene.getroot():
            go = XMLSceneParser.getGameObjectFromXML(xml_go)
            go.transform.parent = root.transform
        
        return root

    @staticmethod
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
            go = XMLSceneParser.getGameObjectFromPrefab(prefab, name)
        else:
            # prefab attribute not set. Use a new game object
            go = GameObject(name=name)
        for go_or_comp in xml:
            # a game object can contain game objects and components
            if go_or_comp.tag == "gameobject":
                xml_go = go_or_comp
                child = XMLSceneParser.getGameObjectFromXML(xml_go)
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

    @staticmethod
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

    @staticmethod
    def getXMLFromScene(scene,):
        """Serialize a whole scene to xml code."""
        pass

    @staticmethod
    def getXMLFromGameObject(game_object):
        pass

    @staticmethod
    def getXMLFromComponent(component):
        print component.getSerializedProperties()