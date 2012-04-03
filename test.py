from xmlsceneparser import XMLSceneParser

roots = XMLSceneParser.read("testscene3.xml")
    
for go in roots:
    pass
    a = go.transform.position
    print a
    #print go.transform.position
    #print go.transform
