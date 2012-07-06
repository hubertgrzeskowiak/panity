# -*- coding: utf-8 -*- 

import wx

class GamePanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        if not kwargs.has_key("name"):
            kwargs["name"] = "game panel"
        wx.Panel.__init__(self, *args, **kwargs)
        game_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(game_panel_sizer)
        self.SetMinSize(wx.Size(200,200))

        # placeholder
        self.panda3d_game_placeholder = wx.StaticText(self, wx.ID_ANY,
                                                      u"This label is a placeholder for a Panda3d window")
        self.panda3d_game_placeholder.Wrap(-1)
        game_panel_sizer.Add(self.panda3d_game_placeholder, 0, wx.EXPAND|wx.ALL, 5)