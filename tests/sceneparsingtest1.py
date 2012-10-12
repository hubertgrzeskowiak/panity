from panity.xmlparser import getSceneFromXMLFile

root = getSceneFromXMLFile("testscene1.xml")
    
for go in root:
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

