import wx
from panityframe import PanityFrame
from panda3dmanager import panda3dmanager
from messagecenter import messageserver

class EditorApplication(object):
    """This is the starting class of the Panity editor. In order to start
    Panity, just import this class and call its only function, 'run'.
    """
    @staticmethod
    def run():

        # Create the default Panda3d instances as subprocesses.
        # Since panda3dmanager is global, the instances are accessible
        # through it from everywhere.
        panda3dmanager.getPanda3dInstance("editor")
        panda3dmanager.getPanda3dInstance("game")

        # Now initialize the GUI in the current process.
        app = wx.App()
        app.SetAppName("Panity")
        app.SetClassName("Panity")
        frame = PanityFrame()
        frame.Show()

        # Keep the global message server ticking, so that we can communicate
        # with the subprocesses.
        frame.messageserver_timer = wx.Timer(frame)
        frame.Bind(wx.EVT_TIMER, messageserver.process, frame.messageserver_timer)
        frame.messageserver_timer.Start(1000.0/60) # 60 times a second

        # Same for the clients in the panda3dmanager.
        frame.messageclients_timer = wx.Timer(frame)
        frame.Bind(wx.EVT_TIMER, panda3dmanager.process, frame.messageclients_timer)
        frame.messageclients_timer.Start(1000.0/60)

        app.MainLoop()