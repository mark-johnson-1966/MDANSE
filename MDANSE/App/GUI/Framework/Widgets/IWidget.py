#MDANSE : Molecular Dynamics Analysis for Neutron Scattering Experiments
#------------------------------------------------------------------------------------------
#Copyright (C)
#2015- Eric C. Pellegrini Institut Laue-Langevin
#BP 156
#6, rue Jules Horowitz
#38042 Grenoble Cedex 9
#France
#pellegrini[at]ill.fr
#goret[at]ill.fr
#aoun[at]ill.fr
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

''' 
Created on Mar 30, 2015

@author: pellegrini
'''

import abc
        
import wx

from MDANSE import REGISTRY
from MDANSE.App.GUI.Framework.Plugins.IPlugin import IPlugin, plugin_parent

class IWidget(wx.Panel):
    
    __metaclass__ = REGISTRY
    
    type = "widget"

    def __init__(self, parent, name, configurable, *args, **kwargs):
        
        wx.Panel.__init__(self, parent, wx.ID_ANY, *args, **kwargs)

        self._parent = parent
        
        self._name = name
        
        self._configurable = configurable
        
        self._configurator = self._configurable.configurators[name]
                        
        self._label = self._configurator.label
                        
        self.initialize()
                        
        self.build_panel()
        
    @property
    def configurator(self):
        return self._configurator

    @property
    def label(self):
        return self._label

    @property
    def name(self):
        return self._name

    @abc.abstractmethod
    def initialize(self):
        pass

    @abc.abstractmethod
    def get_widget_value(self):
        pass
                
    @abc.abstractmethod
    def set_widget_value(self, value):
        pass

    @abc.abstractmethod
    def add_widgets(self):
        pass
    
    def has_parent(self, target):
            
        if self == target:
            return True
        
        if self.TopLevelParent == self:
            return False
        
        return self.has_parent(self.Parent, target)    

    def build_panel(self):        

        self._staticBox = wx.StaticBox(self, wx.ID_ANY, label=self.label)

        self._staticBoxSizer = wx.StaticBoxSizer(self._staticBox, wx.VERTICAL)
                
        self._widgetPanel = wx.Panel(self, wx.ID_ANY)

        self._widgetPanelSizer = self.add_widgets()
        
        self._widgetPanel.SetSizer(self._widgetPanelSizer)
        
        self._staticBoxSizer.Add(self._widgetPanel, 1, wx.ALL|wx.EXPAND, 0)
        
        self.SetSizer(self._staticBoxSizer)
                
    def get_value(self):
        
        return self.get_widget_value()
