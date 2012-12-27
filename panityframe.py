# -*- coding: utf-8 -*- 
import wx
from wx.lib.agw import aui

from inspectorpanel import InspectorPanel
from pandaviewport import PandaViewport
from messagecenter import messageserver

class PanityFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__ (self, None, wx.ID_ANY, u"Panity Editor", wx.DefaultPosition, wx.Size(800,600),
            wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL|wx.EXPAND, "panity main frame")

        self.SetTitle("Panity")

        top_level_sizer = wx.FlexGridSizer(2, 1, 0, 0)
        top_level_sizer.AddGrowableCol(0)
        top_level_sizer.AddGrowableRow(1)
        top_level_sizer.SetFlexibleDirection(wx.BOTH)
        top_level_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        self.SetSizer(top_level_sizer)

        # Menu
        self.menubar = wx.MenuBar(0)
        self.file_menu = wx.Menu()
        self.m_menuItem7 = wx.MenuItem(self.file_menu, wx.ID_ANY, u"MyMenuItem", wx.EmptyString, wx.ITEM_NORMAL)
        self.file_menu.AppendItem(self.m_menuItem7)
        
        self.menubar.Append(self.file_menu, u"File") 
        
        self.m_menu5 = wx.Menu()
        self.m_menuItem8 = wx.MenuItem(self.m_menu5, wx.ID_ANY, u"MyMenuItem", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu5.AppendItem(self.m_menuItem8)
        
        self.menubar.Append(self.m_menu5, u"MyMenu") 
        
        self.m_menu6 = wx.Menu()
        self.m_menuItem9 = wx.MenuItem(self.m_menu6, wx.ID_ANY, u"MyMenuItem", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu6.AppendItem(self.m_menuItem9)
        
        self.menubar.Append(self.m_menu6, u"MyMenu") 
        
        self.SetMenuBar(self.menubar)

        
        # Statusbar
        self.statusbar = self.CreateStatusBar(1, wx.ST_SIZEGRIP, wx.ID_ANY)

        
        # Toolbar
        toolbar_sizer = wx.FlexGridSizer(1, 0, 0, 0)
        self.toolbar = wx.Panel(self, name="toolbar")
        self.toolbar.SetSizer(toolbar_sizer)
        
        self.pause_button = wx.Button(self.toolbar, wx.ID_ANY, u"pause", wx.DefaultPosition, wx.DefaultSize)
        toolbar_sizer.Add(self.pause_button)
        
        self.play_button = wx.Button(self.toolbar, wx.ID_ANY, u"play", wx.DefaultPosition, wx.DefaultSize)
        toolbar_sizer.Add(self.play_button)
        
        self.stop_button = wx.Button(self.toolbar, wx.ID_ANY, u"stop", wx.DefaultPosition, wx.DefaultSize)
        toolbar_sizer.Add(self.stop_button)
        
        top_level_sizer.Add(self.toolbar, 0, wx.EXPAND|wx.ALL, 5)
        

        # Content Panel (consisting of a few panels all managed by an auimanager)
        content_sizer = wx.BoxSizer(wx.VERTICAL)
        self.content_panel = wx.Panel(self, name="content panel")
        self.content_panel.SetSizer(content_sizer)
        top_level_sizer.Add(self.content_panel, 0, wx.EXPAND|wx.ALL, 5)

        self.mgr = aui.AuiManager(self.content_panel, agwFlags=aui.AUI_MGR_DEFAULT|aui.AUI_MGR_AUTONB_NO_CAPTION|
                                                               aui.AUI_MGR_WHIDBEY_DOCKING_GUIDES|
                                                               aui.AUI_MGR_VENETIAN_BLINDS_HINT|aui.AUI_MGR_HINT_FADE)
        self.mgr.SetAutoNotebookStyle(aui.AUI_NB_TOP|aui.AUI_NB_TAB_MOVE|aui.AUI_NB_CLOSE_BUTTON)

        
        # Game Panel
        self.game_panel = PandaViewport("game", self.content_panel)
        self.game_panel.SetMinSize(wx.Size(200,200))
        content_sizer.Add(self.game_panel, 1, wx.EXPAND)


        # Editor Pane
        self.editor_panel = PandaViewport("editor", self.content_panel)
        self.editor_panel.SetMinSize(wx.Size(200,200))
        content_sizer.Add(self.editor_panel, 1, wx.EXPAND)
        
        # Resources Pane
        resources_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.resources_panel = wx.Panel(self.content_panel, name="resources_panel")
        self.resources_panel.SetMinSize(wx.Size(200,200))
        self.resources_panel.SetSizer(resources_panel_sizer)
        
        self.resources_dir = wx.TreeCtrl(self.resources_panel, style=wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT)
        resources_root = self.resources_dir.AddRoot("resources")
        items = ["test1", "test2", "test3"]
        for item in items:
            self.resources_dir.AppendItem(resources_root, item)
        resources_panel_sizer.Add(self.resources_dir, 1, wx.EXPAND|wx.ALL, 5)

        content_sizer.Add(self.resources_panel, 1, wx.EXPAND)


        # Project Panel
        project_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.project_panel = wx.Panel(self.content_panel, name="project panel")
        self.project_panel.SetMinSize(wx.Size(200,200))
        self.project_panel.SetSizer(project_panel_sizer)
        
        self.project_tree = wx.TreeCtrl(self.project_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT)
        root = self.project_tree.AddRoot("render")
        self.project_tree.AppendItem(root, "item1")
        self.project_tree.AppendItem(root, "item2") 
        project_panel_sizer.Add(self.project_tree, 1, wx.EXPAND)

        content_sizer.Add(self.project_panel, 1, wx.EXPAND)

        
        # Inspector Panel
        self.inspector_panel = InspectorPanel(self.content_panel)
        content_sizer.Add(self.inspector_panel, 1, wx.EXPAND)
        

        
        # Add all panes to the manager
        self.mgr.AddPane(self.resources_panel,
                         aui.AuiPaneInfo().Left().Caption("Resources").Layer(2).MinSize(self.resources_panel.GetMinSize()))
        self.mgr.AddPane(self.project_panel,
                         aui.AuiPaneInfo().Left().Caption("Project").Layer(2).MinSize(self.project_panel.GetMinSize()))
        self.mgr.AddPane(self.inspector_panel,
                         aui.AuiPaneInfo().Right().Caption("Inspector").Layer(1).MinSize(self.inspector_panel.GetMinSize()))
        self.mgr.AddPane(self.game_panel,
                         aui.AuiPaneInfo().Center().Caption("Game").Layer(0).MinSize(self.game_panel.GetMinSize()).MaximizeButton())
        self.mgr.AddPane(self.editor_panel,
                         aui.AuiPaneInfo().Bottom().Caption("Editor").Layer(0).MinSize(self.editor_panel.GetMinSize()).MaximizeButton())
        self.mgr.Update()

    def Destroy(self):
        """Clean up the AUI Manager. Do not put this into an EVT_WINDOW_DESTROY event handler.
        It won't work.
        """
        self.mgr.Destroy()
        wx.Frame.Destroy(self)
