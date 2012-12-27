import sys
import os
from multiprocessing import Process, Pipe
from multiprocessing.dummy.connection import Pipe as FakePipe

import wx

from messagecenter import *
from panda3dmanager import panda3dmanager


class PandaViewport(wx.Panel):
    """A special Panel which holds an embedded Panda3d window.
    On initialisation (but not until the panel is shown) a new window is
    created for the given p3d_name (which is a name of a Panda3d instance in
    the panda3dmanager).
    """
    def __init__(self, p3d_name, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        self.p3d_name = p3d_name
        self.p3dinstance = panda3dmanager.getPanda3dInstance(p3d_name)
        self.messageclient = self.p3dinstance.messageclient
        self.messageclient.addListener(self.UImessageProcessor, UI)
        # The window is is set in initialize.
        self.window_id = None

        # See __doc__ of initialize() for this callback.
        self.GetTopLevelParent().Bind(wx.EVT_SHOW, self._onShow)

    def initialize(self):
        """This method requires the top most window to be visible, i.e. you called Show()
        on it. Call initialize() after the whole Panel has been laid out and the UI is mostly done.
        It will spawn a new process with a new Panda3D window and this Panel as host.
        """
        assert self.GetHandle() != 0

        w, h = self.ClientSize.GetWidth(), self.ClientSize.GetHeight()
        self.window_id = panda3dmanager.openWindow(self.p3dinstance,
                                                   w, h, self.GetHandle())
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
        if self.window_id is None:
            return
        # when the wx-panel is resized, fit the panda3d window into it
        w, h = event.GetSize().GetWidth(), event.GetSize().GetHeight()
        self.messageclient.unicast(self.p3d_name, ResizeWindowRequest(self.window_id, w, h))

        self.GetTopLevelParent().Refresh()
 
    def _onDefocus(self, event):
        f = wx.Window.FindFocus()
        if f:
            # This makes Panda lose keyboard focus
            f.GetTopLevelParent().Raise()

    def _onDestroy(self, event):
        pass
        # TODO!

    def UImessageProcessor(self, message):
        p = message.payload
    
        if p.req_spec == FOCUS_WINDOW:
            if p.window_id == self.window_id:
                self.SetFocus()

# TODO
# Test
# if __name__ == "__main__":
#     app = wx.App(redirect=False)
#     frame = wx.Frame(parent=None, size=wx.Size(500,500))
#     p = PandaViewport(parent=frame)
#     t = wx.TextCtrl(parent=frame)
#     sizer = wx.FlexGridSizer(2, 1) # two rows, one column
#     sizer.AddGrowableRow(0) # make first row growable
#     sizer.AddGrowableCol(0) # make first column growable
#     sizer.SetFlexibleDirection(wx.BOTH)
#     sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
#     sizer.Add(p, flag=wx.EXPAND)
#     sizer.Add(t, flag=wx.EXPAND)
#     frame.SetSizer(sizer)
#     frame.Show()
#     app.MainLoop()
