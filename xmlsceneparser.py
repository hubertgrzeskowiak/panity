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
        """Read a scene from an xml file, create it and return a list of the
        root game objects.
        """
        # TODO: get the path from vfs and os-specific (appropriate for etree)
        xmlscene = etree.parse(source)
        if validate:
            validateScene(xmlscene.getroot())
        roots = []
        for xml_go_root in xmlscene.getroot():
            roots.append(XMLSceneParser._appendGameObject(xml_go_root))
        return roots

    @staticmethod
    def _appendGameObject(xml_child, parent=None):
        """Create a game object from xml and append it as child of the parent
        game object. This function calls itself recursively. Prefabs are loaded
        using self._getGameObjectFromPrefab().
        """

        prefab = xml_child.get("prefab")
        name = xml_child.get("name")
        if prefab:
            go = _getGameObjectFromPrefab(prefab, name)
        else:
            go = GameObject(name=name)
        for go_or_comp in xml_child:
            if go_or_comp.tag == "gameobject":
                xml_go = go_or_comp
                XMLSceneParser._appendGameObject(xml_go, go)
            elif go_or_comp.tag == "component":
                xml_comp = go_or_comp
                comp = go.getComponent(xml_comp.get("type"))
                # WARNING: Here the API differs from that of Unity.
                # Get back here after thinking a bit about prefabs and their
                # connections to objects.
                if not comp:
                    comp = go.addComponent(xml_comp)
                for option in xml_comp:
                    setattr(comp, option, option.text)
        go.name = name
        if parent:
            go.parent = parent
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
