import wx

from .. import gamePlugin as gp
from wxExtra import utils as wxUtils


ID_CREATE_BOX = wx.NewId()
ID_CREATE_CONE = wx.NewId()


class EditorPlugin( gp.GamePlugin ):
        
    def OnInit( self ):
        gp.GamePlugin.OnInit( self )
        
        # Build primitives menu
        self.mPrim = wx.Menu()
        self.mPrim.Append( ID_CREATE_BOX, '&Box' )
        self.mPrim.Append( ID_CREATE_CONE, '&Cone' )
        
        # Bind primitives menu events
        wxUtils.IdBind( self.ui, wx.EVT_MENU, ID_CREATE_BOX, self.ui.OnCreate, gp.TAG_BOX )
        wxUtils.IdBind( self.ui, wx.EVT_MENU, ID_CREATE_CONE, self.ui.OnCreate, gp.TAG_CONE )
        
        # Append to create menu
        self.ui.mCreate.AppendSeparator()
        self.ui.mCreate.AppendSubMenu( self.mPrim, '&Primitives' )