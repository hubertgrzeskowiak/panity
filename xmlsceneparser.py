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
    def read(source, validate=True):
        """Read a scene from an xml file, create it and return a root game object.
        AssertionErrors can be thrown when validation fails.
        """
        # TODO: get the path from vfs and os-specific (appropriate for etree)
        xmlscene = etree.parse(source)
        if validate:
            validateScene(xmlscene.getroot())
        root = GameObject(source.rsplit(".xml", 1)[0])
        for xml_go in xmlscene.getroot():
            go = XMLSceneParser._appendGameObject(xml_go)
            go.transform.parent = root.transform
        return root

    @staticmethod
    def _appendGameObject(xml_child, parent=None):
        """Create a game object from xml and append it as child of the parent
        game object. This function calls itself recursively. Prefabs are loaded
        using self._getGameObjectFromPrefab().
        """

        # prefab means we should create an instance of a prefab and extend it
        prefab = xml_child.get("prefab")
        name = xml_child.get("name")
        if prefab:
            go = XMLSceneParser._getGameObjectFromPrefab(prefab, name)
        else:
            # prefab attribute not set. Use a new game object
            go = GameObject(name=name)
        for go_or_comp in xml_child:
            # a game object can contain game objects and components
            if go_or_comp.tag == "gameobject":
                xml_go = go_or_comp
                XMLSceneParser._appendGameObject(xml_go, go)
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
        if parent:
            go.transform.parent = parent.transform
        else:
            return go

    @staticmethod
    def _getGameObjectFromPrefab(prefab_source, name):
        """Create a game object from a prefab, which corresponds to a
        prefab file from the prefabs package.
        """
        raise NotImplementedError
        # TODO:
        # import prefab
        # instantiate it
        # call Object.instantiate()
        # or
        # call PrefabUtility.getPrefabObject()

    @staticmethod
    def write(source, data):
        """Write a scene to xml file. data is an iterable of the root game
        objects.
        """
        # TODO
        pass
