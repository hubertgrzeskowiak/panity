import sys
import os
from multiprocessing import Process, Pipe

import wx

from messagecenter import *
from embeddedpanda3dapp import EmbeddedPanda3dApp
from gameobject import GameObject

class PandaViewport(wx.Panel):
    """A special Panel which holds an embedded Panda3d window."""
    def __init__(self, app_type, *args, **kwargs):
        """app_type should be a string, a name for the p3d app, e.g. "preview"
        or "editor".
        """
        wx.Panel.__init__(self, *args, **kwargs)

        self.app_type = app_type

        local_pipe, remote_pipe = FakePipe()
        self.messageclient = MessageClient(local_pipe)
        self.messageclient.addListener(self.messageProcessor)
        self.messageclient_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.messageclient.process, self.messageclient_timer)

        messageserver.connectPipe(self.app_type+" gui", remote_pipe)

        # See __doc__ of initialize() for this callback
        self.GetTopLevelParent().Bind(wx.EVT_SHOW, self._onShow)


    def initialize(self):
        """This method requires the top most window to be visible, i.e. you called Show()
        on it. Call initialize() after the whole Panel has been laid out and the UI is mostly done.
        It will spawn a new process with a new Panda3D window and this Panel as parent.
        """
        assert self.GetHandle() != 0
        server_pipe, pandas_pipe = Pipe()
        w, h = self.ClientSize.GetWidth(), self.ClientSize.GetHeight()
        self.panda_process = Process(target=EmbeddedPanda3dApp, args=(
            self.GetHandle(), pandas_pipe, self.app_type, w, h))
        self.panda_process.start()
        messageserver.connectPipe(self.app_type, server_pipe)

        self.messageclient_timer.Start(1000.0/60) # 60 times a second

        self.Bind(wx.EVT_SIZE, self._onResize)
        self.Bind(wx.EVT_KILL_FOCUS, self._onDefocus)
        self.Bind(wx.EVT_WINDOW_DESTROY, self._onDestroy)
        self.SetFocus()

    def _onShow(self, event):
        if event.GetShow() and self.GetHandle():
            # M$ Windows makes problems when initializing here. Call it after this function.
            if os.name == "nt":
                wx.CallAfter(self.initialize)
            # All other OSes should be okay with instant init.
            else:
                self.initialize()
        event.Skip()

    def _onResize(self, event):
        # when the wx-panel is resized, fit the panda3d window into it
        w, h = event.GetSize().GetWidth(), event.GetSize().GetHeight()
        self.messageclient.unicast(self.app_type, UIRequest("resizeWindow", [w, h]))

        self.GetTopLevelParent().Refresh()
 
    def _onDefocus(self, event):
        f = wx.Window.FindFocus()
        if f:
            # This makes Panda lose keyboard focus
            f.GetTopLevelParent().Raise()

    def _onDestroy(self, event):
        messageserver.detachPipeByName(self.app_type)
        # Give Panda a second to close itself and terminate it if it doesn't
        self.panda_process.join(1)
        if self.panda_process.is_alive():
            self.panda_process.terminate()

    def messageProcessor(self, message):
        p = message.payload
        if p.req_type == UI:
            if p.command == "setFocus":
                self.SetFocus()
        elif p.req_type == COMMAND:
            if isinstance(p, AddGameObjectRequest):
                print self.app_type, "adding game object", p.idnr

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
