#!/usr/bin/env python2
"""XML validator for scenes and prefabs.
Multple xml files can be passed to this module at the command line.
Whether a file is considered a scene or prefab depends on the root tag.
Scenes should have 'scene' as root tag and prefabs 'gameobject'.
"""

import sys
try:
    from xml.etree import cElementTree as etree
except ImportError:
    from xml.etree import ElementTree as etree


def validateScene(scene):
    """scene should be an xml element (-tree) of type scene."""
    # root tag needs to be a "scene"
    assert scene.tag == "scene", "root must be 'scene'"
    for go in scene:
        # all children of root must be "gameobject"s
        assert go.tag == "gameobject", "a scene must contain game objects only"
        validateGameObject(go)

def validateGameObject(go):
    """go should be an xml element (-tree) of type gameobject."""
    assert go.tag == "gameobject", "game object expected"
    components = []
    for go_or_comp in go:
        # all children of game objects must be
        # either game objects or components
        if go_or_comp.tag == "gameobject":
            validateGameObject(go_or_comp)
        elif go_or_comp.tag == "component":
            validateComponent(go_or_comp)
            if go_or_comp.get("type") in components:
                print "".join(["WARNING! game object '{}' has the '{}' ",
                      "component multiple times!"]).format(
                      go.get("name"), go_or_comp.get("type"))
            components.append(go_or_comp.get("type"))

        else:
            raise AssertionError("a game object must contain game "+\
                "objects and/or components only")

def validateComponent(comp):
    """comp should be an xml element (-tree) of type component."""
    assert comp.tag == "component", "component expected"
    assert comp.get("type") is not None, "components must have a type attribute"
    for tag in comp:
        assert tag.tag not in ["gameobject", "component"], "components "+\
            "must not contain game objects or components"

def validate(anything):
    """Determine if we have a scene, game object or component and pass
    the xml tree to the right function.
    'anything' should be an xml element (-tree) of any type.
    If the element in question is not a scene, gameobject or component,
    an AssertionError is raised.
    """
    if anything.tag == "scene":
        validateScene(anything)
    elif anything.tag == "gameobject":
        validateGameObject(anything)
    elif anything.tag == "component":
        validateComponent(anything)
    else:
        raise AssertionError("Cannot validate {}, as it's no "+\
                "expected format.".format(anything))


# command line interface
if __name__ == "__main__":
    files = sys.argv[1:]
    if not files:
        print "Usage:\n\n\txmlvalidator.py scenefile.xml prefab.xml ...\n"
        sys.exit(-1)
    first = True
    for f in files:
        # draw a line between all file checks
        if first:
            first = False
        else:
            print "-"*23
            
        print "Testing {}".format(f)
        try:
            validate(etree.parse(f).getroot())
            print "{} OK".format(f)
        except AssertionError as a:
            print a
