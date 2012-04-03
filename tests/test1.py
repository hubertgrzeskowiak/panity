from xmlsceneparser import XMLSceneParser

roots = XMLSceneParser.read("testscene1.xml")
    
for go in roots:
    print go
    for child in go:
        print "- "+str(child)

    # this is actually the same;
    #children = go.transform.getChildren()
    #for child in children:
    #    print "- "+str(child.game_object)

    # and this:
    #for child in go.transform:
    #    print "- "+str(child.game_object)

