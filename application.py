class BuildSettings(object):
    # list of panda3d.core.Filename
    scenes = []
    # additional settings could be optimizations or target platforms

class LevelLoadingError(Exception):
    pass

class Application(object):
    # list of outputs of scene parser
    active_scenes = []

    @staticmethod
    def run():
        if len(BuildSettings.scenes) < 1:
            return
        scene = XMLSceneParser(BuildSettings.scenes[0])
        Application.active_scenes.append(scene)
        # create a scene graph
        # create a camera if there is none
        # start the task for the game
        # offer ways to pause and stop

    @staticmethod
    def loadLevel(name_or_index):
        # iterate over all objects in the current scene
        # check the attribute "dont_destroy_on_load"
        # destroy those objects which do not have that attribute
        # Application.active_scenes = []
        # call loadLevelAdditive()
        raise NotImplementedError
    
    @staticmethod
    def loadLevelAdditive(name_or_index):
        # first try to use arg as index
        try:
            scene = BuildSettings.scenes[name_or_index]
        except TypeError:
            # then as full filename
            for s in BuildSettings.scenes:
                if s.getBasename == name_or_index:
                    print s
                    scene = s
                    break
            if not scene:
                # then as basename (without extension)
                for s in BuildSettings.scenes:
                    if s.getBasenameWoExtension == name_or_index:
                        print s
                        scene = s
                        break
        if not scene:
            raise LevelLoadingError("level {} couldn't be found".format(
                                                                 name_or_index))
        
        if s.getExtension() in ("xml", "scene"):
            scene = XMLSceneParser(s)
