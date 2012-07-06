# -*- coding: utf-8 -*- 

import wx

class InspectorPanel(wx.ScrolledWindow):
    def __init__(self, *args, **kwargs):
        if not kwargs.has_key("name"):
            kwargs["name"] = "inspector panel"
        inspector_sizer = wx.FlexGridSizer(2, 1, 0, 0)
        inspector_sizer.AddGrowableCol(0)
        inspector_sizer.SetFlexibleDirection(wx.BOTH)
        inspector_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetMinSize(wx.Size(250,200))
        self.SetSizer(inspector_sizer)
        

        # Sample components
        self.current_item_label = wx.StaticText(self, wx.ID_ANY, u"Object Name")
        self.current_item_label.Wrap(-1)
        
        inspector_sizer.Add(self.current_item_label, 0, wx.ALL, 5)
        
        component_1_sizer = wx.FlexGridSizer(0, 1, 0, 0)
        component_1_sizer.AddGrowableCol(0)
        component_1_sizer.SetFlexibleDirection(wx.BOTH)
        component_1_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        self.component_1 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.component_1.SetSizer(component_1_sizer)
        
        self.component_1_headline = wx.Panel(self.component_1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.component_1_headline.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR))

        
        component_1_headline_sizer = wx.FlexGridSizer(1, 0, 0, 0)
        component_1_headline_sizer.AddGrowableCol(2)
        component_1_headline_sizer.SetFlexibleDirection(wx.BOTH)
        component_1_headline_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_ALL)
        
        self.m_checkBox4 = wx.CheckBox(self.component_1_headline, wx.ID_ANY, u"Component 1", wx.DefaultPosition, wx.DefaultSize, 0)
        component_1_headline_sizer.Add(self.m_checkBox4, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
        
        component_1_headline_sizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        
        self.m_button7 = wx.Button(self.component_1_headline, wx.ID_ANY, u"toggle visibility", wx.DefaultPosition, wx.DefaultSize, 0)
        component_1_headline_sizer.Add(self.m_button7, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        
        
        self.component_1_headline.SetSizer(component_1_headline_sizer)
        component_1_sizer.Add(self.component_1_headline, 1, wx.EXPAND, 5)
        
        
        
        inspector_sizer.Add(self.component_1, 1, wx.BOTTOM|wx.EXPAND, 2)
        
        self.component_2 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        component_2_sizer = wx.FlexGridSizer(0, 1, 0, 0)
        component_2_sizer.AddGrowableCol(0)
        component_2_sizer.SetFlexibleDirection(wx.BOTH)
        component_2_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        
        self.component_2_headline = wx.Panel(self.component_2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.component_2_headline.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR))
        
        component_1_headline_sizer1 = wx.FlexGridSizer(1, 0, 0, 0)
        component_1_headline_sizer1.AddGrowableCol(2)
        component_1_headline_sizer1.SetFlexibleDirection(wx.BOTH)
        component_1_headline_sizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_ALL)
        
        self.m_checkBox41 = wx.CheckBox(self.component_2_headline, wx.ID_ANY, u"Component 2", wx.DefaultPosition, wx.DefaultSize, 0)
        component_1_headline_sizer1.Add(self.m_checkBox41, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
        
        component_1_headline_sizer1.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        
        self.m_button71 = wx.Button(self.component_2_headline, wx.ID_ANY, u"toggle visibility", wx.DefaultPosition, wx.DefaultSize, 0)
        component_1_headline_sizer1.Add(self.m_button71, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        
        
        self.component_2_headline.SetSizer(component_1_headline_sizer1)
        self.component_2_headline.Layout()
        component_1_headline_sizer1.Fit(self.component_2_headline)
        component_2_sizer.Add(self.component_2_headline, 1, wx.EXPAND, 5)
        
        
        self.component_2.SetSizer(component_2_sizer)
        self.component_2.Layout()
        component_2_sizer.Fit(self.component_2)
        inspector_sizer.Add(self.component_2, 1, wx.BOTTOM|wx.EXPAND, 2)
        
        self.component_3 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        component_3_sizer = wx.FlexGridSizer(0, 1, 0, 0)
        component_3_sizer.AddGrowableCol(0)
        component_3_sizer.SetFlexibleDirection(wx.BOTH)
        component_3_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        
        self.component_3_headline = wx.Panel(self.component_3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.component_3_headline.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR))
        
        component_1_headline_sizer11 = wx.FlexGridSizer(1, 0, 0, 0)
        component_1_headline_sizer11.AddGrowableCol(2)
        component_1_headline_sizer11.SetFlexibleDirection(wx.BOTH)
        component_1_headline_sizer11.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_ALL)

        component_1_headline_sizer11.AddSpacer((24, 0), 1, wx.EXPAND, 5)
        
        self.m_staticText11 = wx.StaticText(self.component_3_headline, wx.ID_ANY, u"Component 3", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText11.Wrap(-1)
        component_1_headline_sizer11.Add(self.m_staticText11, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        component_1_headline_sizer11.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        
        self.m_button711 = wx.Button(self.component_3_headline, wx.ID_ANY, u"toggle visibility", wx.DefaultPosition, wx.DefaultSize, 0)
        component_1_headline_sizer11.Add(self.m_button711, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        self.component_3_headline.SetSizer(component_1_headline_sizer11)
        component_1_headline_sizer11.Fit(self.component_3_headline)
        component_3_sizer.Add(self.component_3_headline, 1, wx.EXPAND, 5)

        self.component_3.SetSizer(component_3_sizer)
        inspector_sizer.Add(self.component_3, 1, wx.BOTTOM|wx.EXPAND, 2)