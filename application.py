class BuildSettings(object):
    # format: ?
    scenes = []

class Application(object):
    @staticmethod
    def loadLevel(name_or_index):
        # iterate over all objects in the current scene
        # check the attribute "dont_destroy_on_load"
        # destroy those objects which do not have that attribute
        # 
        pass
