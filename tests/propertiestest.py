from panity.properties import *

class C(object):
    f1 = FloatProperty()
    f2 = FloatProperty(default=1.0)



def checkAssignment():

    c1 = C()
    c2 = C()

    assert c1.f1 == 0.0
    c1.f1 = "string"
    assert c1.f1 == 0.0
    c1.f1 = "1.34"
    assert c1.f1 == 1.34
    c1.f1 = -1000
    assert c1.f1 == -1000.0
    try:
        assert C.f1
    except AttributeError:
        pass
    assert c2.f1 == 0.0
    c2.f1 = 100.2
    assert c2.f1 == 100.2
    assert c2.f2 == 1.0
    c2.f2 = -3.1415
    assert c2.f2 == -3.1415


def checkListeners():
    
    class D(C):
        def __init__(self):
            D.f1.addListener(self, self.printF1)
            D.f2.addListener(self, self.printF2)
            print "you should now see three lines of jibberish,"
            print "if you don't, consider it an error:"
            self.f1 = 3.0
            self.f2 = 55.22
        def printF1(self, value):
            print "f1 property was changed: "+str(value)
        def printF2(self, value):
            print "f2 property was changed: "+str(value)
    
    d = D()
    d.f1 = 4.0
    d.f1 = 4.0 # callback only spawns on change, but this is none



checkAssignment()
checkListeners()
print "success"