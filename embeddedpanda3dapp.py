from direct.task import Task
from pandac.PandaModules import WindowProperties
from pandac.PandaModules import loadPrcFileData
from direct.showbase.ShowBase import ShowBase

from messagecenter import *
from gameobject import GameObject
from scenegraph import Root

class EmbeddedPanda3dApp(object):
    def __init__(self, handle, pipe, app_type, width=300, height=300):
        """Arguments:
        handle -- parent window handle
        pipe -- multiprocessing pipe for communication
        width -- width of the window
        height -- height of the window
        """

        self.gameobjects = []

        self.pipe = pipe
        self.messageclient = MessageClient(self.pipe)
        self.app_type = app_type

        loadPrcFileData("", "window-type none")
        loadPrcFileData("", "audio-library-name null")

        self.base = ShowBase()
        wp = WindowProperties()
        wp.setOrigin(0, 0)
        wp.setSize(width, height)
        wp.setParentWindow(handle)
        self.base.openDefaultWindow(props=wp, gsg=None)

        self.messageclient.addListener(self.messageProcessor)

        def processTask(task):
            self.messageclient.process()
            return task.cont
        self.base.addTask(processTask, "message processor",
                          appendTask=False)

        self.base.accept("mouse1-up", self.focus)
        #self.base.accept("a", lambda: self.addGameObject("test object"))
        #self.base.accept("d", self.removeLastGameObject)

        # TODO: Wrap this around a try..except block and notify the main
        # process on errors.
        self.base.run()

    def messageProcessor(self, message):
        p = message.payload
        if p.req_type == UI:
            if p.command == "resizeWindow":
                self.resizeWindow(*p.args)
        # TODO: move this to subclasses
        elif p.req_type == COMMAND:
             if isinstance(p, AddGameObjectRequest):
                self.addRequestedGameObject(p.idnr)

    def focus(self):
        """Bring Panda3d to foreground, so that it gets keyboard focus.
        Also send a message to wx, so that it doesn't render a widget focused.
        We also need to say wx that Panda now has focus, so that it can notice when
        to take focus back.
        """
        wp = WindowProperties()
        # TODO: test this on Windows
        wp.setForeground(True)
        self.base.win.requestProperties(wp)
        # We request focus (and probably already have keyboard focus), so make wx
        # set it officially. This prevents other widgets from being rendered focused.
        self.messageclient.unicast(self.app_type+" gui", UIRequest("setFocus"))

    def resizeWindow(self, width, height):
        old_wp = self.base.win.getProperties()
        if old_wp.getXSize() == width and old_wp.getYSize() == height:
            return
        wp = WindowProperties()
        wp.setOrigin(0, 0)
        wp.setSize(width, height)
        self.base.win.requestProperties(wp)

    def close(self):
        sys.exit()

    def addGameObject(self, name=None):
        """Add a new game object to the scene."""
        # TODO: we should send a real id instead of name or None
        self.messageclient.others(AddGameObjectRequest(name))
        self.addRequestedGameObject(name)

    def addRequestedGameObject(self, name=None):
        """Add a game object to the local scene (only this P3D instance)."""
        go = GameObject(name)
        go.transform.parent = Root(render)
        self.gameobjects.append(go)
        #mesh = go.addComponent("Mesh")
        #mesh.path = "smiley"
        #go.transform.local_position = (0, 13, 0)

    #def removeLastGameObject(self):
    #    if self.gameobjects != []:
    #        go = self.gameobjects.pop()
    #        go.destroy()