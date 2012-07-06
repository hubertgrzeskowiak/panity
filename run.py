import wx
from panityframe import PanityFrame

if __name__ == "__main__":
    app = wx.App()
    
    frame = PanityFrame(None)
        
    frame.Show()
    app.MainLoop()