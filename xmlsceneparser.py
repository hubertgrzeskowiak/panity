try:
    from xml.etree import cElementTree as etree
except ImportError:
    from xml.etree import ElementTree as etree

from parserinterface import ParserInterface
from xmlvalidator import validateScene
from gameobject import GameObject
from component import Component
import components

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

        prefab = xml_child.get("prefab")
        name = xml_child.get("name")
        if prefab:
            go = XMLSceneParser._getGameObjectFromPrefab(prefab, name)
        else:
            # prefab attribute not set
            go = GameObject(name=name)
        for go_or_comp in xml_child:
            # a game object can contain game objects and components
            if go_or_comp.tag == "gameobject":
                xml_go = go_or_comp
                XMLSceneParser._appendGameObject(xml_go, go)
            elif go_or_comp.tag == "component":
                xml_comp = go_or_comp
                # does the GO already have such a component?
                comp = go.getComponent(xml_comp.get("type"))
                if not comp:
                    # if not, create it
                    comp = go.addComponent(xml_comp.get("type"))
                else:
                    print "".join(["second appearence of component '{}' ",
                                   "in game object '{}' ignored"]).format(
                                   xml_comp.get("type"), go.name)
                for option in xml_comp:
                    setattr(comp, option, option.text)
        go.name = name
        if parent:
            go.transform.parent = parent.transform
        else:
            return go

    @staticmethod
    def _getGameObjectFromPrefab(prefab_name, name):
        """Create a game object from a prefab name, which corresponds to a
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
