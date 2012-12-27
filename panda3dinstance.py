from direct.task import Task
from pandac.PandaModules import WindowProperties
from pandac.PandaModules import loadPrcFileData
from direct.showbase.ShowBase import ShowBase

from messagecenter import *
from gameobject import GameObject
from scenegraph import Root


# TODO: tell the difference between methods depending on their effects.
# E.g. some communicate with wx, others do not. Some are for special windows only, others not.
class Panda3dInstance(object):
    """This class normally is instantiated in a subprocess, where it spawns
    Panda3D.

    If you aren't 100% sure what you're doing, use the Panda3dManager instead.
    """
    def __init__(self, pipe, name):
        """Arguments:
        pipe -- Multiprocessing pipe for communication. See messagecenter
                module for more info.
        name -- Name of this instance.
        """

        #self.gameobjects = []

        self.messageclient = MessageClient(pipe)
        self.name = name
        self.windows = {}

        # set a few default settings
        loadPrcFileData("", "window-type none")
        loadPrcFileData("", "audio-library-name null")

        # initiate Panda3D
        self.base = ShowBase()
        
        # start processing incoming requests
        self.messageclient.addListener(self.UImessageProcessor, req_type=UI)

        # The request processing task should never stop as long as the
        # subprocess exists. This is a wrapper that ensures that and saves
        # us from confusion about "hey, why has this message processing
        # stopped?!"
        def messageProcessor(task):
            self.messageclient.process()
            return task.cont
        self.base.addTask(messageProcessor, "message processor")

        # As soon as the user clicks the window, it should get focus, like any other widget.
        self.base.accept("mouse1", self.focus)

        # TODO: Wrap this around a try..except block and notify the main
        # process on errors.
        self.base.run()

    def getWindowUnderPointer(self):
        """Returns the key from self.windows of the window the primary poiter
        currently hovers over.
        """
        for win_id, win in self.windows.iteritems():
            props = win.getProperties()
            pointer = win.getPointer(0)
            if pointer.getInWindow():
                return win_id

    def addWindow(self, handle=None, width=500, height=500):
        """Create a new window showing the scene. Add it to the windows list
        and return it.
        If handle is not None, it is used as parent window.
        """
        wp = WindowProperties()
        wp.setOrigin(0, 0)
        wp.setSize(width, height)
        if handle is not None:
            wp.setParentWindow(handle)
        self.base.openDefaultWindow(props=wp,
                                    type="onscreen",
                                    requireWindow=True)
        return self.base.winList[-1]

    def UImessageProcessor(self, message):
        p = message.payload
        # TODO: look up the req_spec attribute, not class instance
        if p.req_spec == OPEN_WINDOW:
            assert not self.windows.has_key(p.window_id)
            win = self.addWindow(p.handle, p.width, p.height)
            self.windows[p.window_id] = win
        elif p.req_spec == RESIZE_WINDOW:
            self.resizeWindow(p.window_id, p.width, p.height)

    def focus(self, window_id=None):
        """Bring Panda3d to foreground, so that it gets keyboard focus.
        Also send a message to wx, so that it doesn't render a widget focused.
        We also need to say wx that Panda now has focus, so that it can notice when
        to take focus back.

        If window_id is given, that window will be focused, otherwise the one
        the pointer hovers upon. If the pointer doesn't hover over a window,
        a random window is taken. If there is no window, this function does nothing.
        """
        if window_id is None:
            window_id = self.getWindowUnderPointer()
        if window_id is None:
            for win in self.windows.values():
                window_id = win
                break
        if window_id is None:
            return
        wp = WindowProperties()
        wp.setForeground(True)
        self.windows[window_id].requestProperties(wp)
        # We request focus (and probably already have keyboard focus), so make wx
        # set it officially. This prevents other widgets from being rendered focused.
        self.messageclient.unicast(self.name+" gui", FocusWindowRequest(window_id))

    def resizeWindow(self, window_id, width, height):
        """window_id is an index of a window from base.winList."""
        window = self.windows[window_id]
        old_wp = window.getProperties()
        if old_wp.getXSize() == width and old_wp.getYSize() == height:
            return
        wp = WindowProperties()
        wp.setOrigin(0, 0)
        wp.setSize(width, height)
        window.requestProperties(wp)

    def close(self):
        # Everything should be garbage collected this way, except maybe the
        # messaging connection to the server, which will keep sending messages
        # to us.
        # TODO: fix that.
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
