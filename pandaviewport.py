import sys
import os
from multiprocessing import Process, Pipe

import wx

from direct.task import Task
from pandac.PandaModules import WindowProperties
from pandac.PandaModules import loadPrcFileData
from direct.showbase.ShowBase import ShowBase


class PandaViewport(wx.Panel):
    """A special Panel which holds a Panda3d window."""
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        # See __doc__ of initialize() for this callback
        self.GetTopLevelParent().Bind(wx.EVT_SHOW, self.onShow)

    def onShow(self, event):
        if event.GetShow() and self.GetHandle():
            # Windows can't get it right from here. Call it after this function.
            if os.name == "nt":
                wx.CallAfter(self.initialize)
            # All other OSes should be okay with instant init.
            else:
                self.initialize()
        event.Skip()

    def initialize(self):
        """This method requires the top most window to be visible, i.e. you called Show()
        on it. Call initialize() after the whole Panel has been laid out and the UI is mostly done.
        It will spawn a new process with a new Panda3D window and this Panel as parent.
        """
        assert self.GetHandle() != 0
        self.pipe, remote_pipe = Pipe()
        w, h = self.ClientSize.GetWidth(), self.ClientSize.GetHeight()
        self.panda_process = Process(target=Panda3dApp, args=(w, h, self.GetHandle(), remote_pipe))
        self.panda_process.start()

        self.Bind(wx.EVT_SIZE, self.onResize)
        self.Bind(wx.EVT_KILL_FOCUS, self.onDefocus)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)
        self.SetFocus()

        # We need to check the pipe for requests frequently
        self.pipe_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.checkPipe, self.pipe_timer)
        self.pipe_timer.Start(1000.0/60) # 60 times a second

    def onResize(self, event):
        # when the wx-panel is resized, fit the panda3d window into it
        w, h = event.GetSize().GetWidth(), event.GetSize().GetHeight()
        self.pipe.send(["resize", w, h])
 
    def onDefocus(self, event):
        f = wx.Window.FindFocus()
        if f:
            # This makes Panda lose keyboard focus
            f.GetTopLevelParent().Raise()

    def onDestroy(self, event):
        self.pipe.send(["close",])
        # Give Panda a second to close itself and terminate it if it doesn't
        self.panda_process.join(1)
        if self.panda_process.is_alive():
            self.panda_process.terminate()

    def checkPipe(self, event):
        # Panda requested focus (and probably already has keyboard focus), so make wx
        # set it officially. This prevents other widgets from being rendered focused.
        if self.pipe.poll():
            request = self.pipe.recv()
            if request == "focus":
                self.SetFocus()


class Panda3dApp(object):
    def __init__(self, width, height, handle, pipe):
        """Arguments:
        width -- width of the window
        height -- height of the window
        handle -- parent window handle
        pipe -- multiprocessing pipe for communication
        """
        self.pipe = pipe

        loadPrcFileData("", "window-type none")
        loadPrcFileData("", "audio-library-name null")

        ShowBase()
        wp = WindowProperties()
        wp.setOrigin(0, 0)
        wp.setSize(width, height)
        # This causes warnings on Windows
        #wp.setForeground(True)
        wp.setParentWindow(handle)
        base.openDefaultWindow(props=wp, gsg=None)

        self.loadSmiley()

        base.taskMgr.add(self.checkPipe, "check pipe")

        # def printA():
        #     print "'a' key recieved by panda"
        # base.accept("a", printA)
        base.accept("mouse1-up", self.getFocus)

        run()

    def loadSmiley(self):
        s = loader.loadModel("smiley.egg")
        s.reparentTo(render)
        s.setY(5)

    def getFocus(self):
        """Bring Panda3d to foreground, so that it gets keyboard focus.
        Also send a message to wx, so that it doesn't render a widget focused.
        We also need to say wx that Panda now has focus, so that it can notice when
        to take focus back.
        """
        wp = WindowProperties()
        # This causes warnings on Windows
        #wp.setForeground(True)
        base.win.requestProperties(wp)
        self.pipe.send("focus")

    def resizeWindow(self, width, height):
        old_wp = base.win.getProperties()
        if old_wp.getXSize() == width and old_wp.getYSize() == height:
            return
        wp = WindowProperties()
        wp.setOrigin(0, 0)
        wp.setSize(width, height)
        base.win.requestProperties(wp)

    def checkPipe(self, task):
        """This task is responsible for executing actions requested by wxWidgets.
        Currently supported requests with params:
        resize, width, height
        close
        """
        # TODO: only use the last request of a type
        #       e.g. from multiple resize requests take only the latest into account
        while self.pipe.poll():
            request = self.pipe.recv()
            if request[0] == "resize":
                self.resizeWindow(request[1], request[2])
            elif request[0] == "close":
                sys.exit()
        return Task.cont

# Test
if __name__ == "__main__":
    app = wx.App(redirect=False)
    frame = wx.Frame(parent=None, size=wx.Size(500,500))
    p = PandaViewport(parent=frame)
    t = wx.TextCtrl(parent=frame)
    sizer = wx.FlexGridSizer(2, 1) # two rows, one column
    sizer.AddGrowableRow(0) # make first row growable
    sizer.AddGrowableCol(0) # make first column growable
    sizer.SetFlexibleDirection(wx.BOTH)
    sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
    sizer.Add(p, flag=wx.EXPAND)
    sizer.Add(t, flag=wx.EXPAND)
    frame.SetSizer(sizer)
    frame.Show()
    app.MainLoop()
