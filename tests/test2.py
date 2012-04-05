from panity.xmlsceneparser import XMLSceneParser

print "you should now see warnings about multiple components in one game object"
print "-"*20
roots = XMLSceneParser.read("testscene2.xml")
print "-"*20
print "the scene with components:"
for go in roots:
    print go
    for c in go.components:
        print "component: "+str(c)
    for child in go:
        print "- "+str(child)
        for c in child.components:
            print "  component: "+str(c)

    # this is actually the same;
    #children = go.transform.getChildren()
    #for child in children:
    #    print "- "+str(child.game_object)

    # and this:
    #for child in go.transform:
    #    print "- "+str(child.game_object)

