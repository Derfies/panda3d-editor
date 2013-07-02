import wx
import wx.lib.agw.customtreectrl as ct

import pandac.PandaModules as pm
from pandac.PandaModules import NodePath as NP

from .. import commands as cmds
from game.nodes import Attribute as Attr
from sceneGraphBasePanel import SceneGraphBasePanel


class LightLinkerPanel( wx.Panel ):
    
    def __init__( self, *args, **kwargs ):
        wx.Panel.__init__( self, *args, **kwargs )
        
        # Build combo box
        #self.cmboMode = wx.ComboBox( self )
       
        # Build splitter and panels
        self.splt = wx.SplitterWindow( self, style=wx.SP_3DSASH )
        self.splt.SetSashGravity( 0.5 )
        
        self.pnlLeft = SceneGraphBasePanel( self.splt )
        flags = self.pnlLeft.tc.GetAGWWindowStyleFlag()
        self.pnlLeft.tc.SetAGWWindowStyleFlag( flags & ~ct.TR_MULTIPLE )
        self.pnlLeft.filter = pm.Light
        
        self.pnlRight = SceneGraphBasePanel( self.splt )

        # Split the window
        self.splt.SplitVertically( self.pnlLeft, self.pnlRight )
        self.splt.SetMinimumPaneSize( 20 )

        sizer = wx.BoxSizer( wx.VERTICAL )
        #sizer.Add( self.cmboMode, 0, wx.EXPAND )
        sizer.Add( self.splt, 1, wx.EXPAND )
        self.SetSizer( sizer )
        
        # Bind tree control events
        self.pnlLeft.tc.Bind( wx.EVT_TREE_SEL_CHANGED, self.OnLeftTreeSelChanged )
        self.pnlRight.tc.Bind( wx.EVT_TREE_SEL_CHANGED, self.OnRightTreeSelChanged )
        
    def OnLeftTreeSelChanged( self, evt ):
        """
        Select those items in the right list to show the relationship with
        those the user has selected in the left list.
        """
        self.pnlLeft.tc.Freeze()
        
        self.pnlRight.tc.UnselectAll()
        items = self.pnlLeft.tc.GetSelections()
        if items:
            light = items[0].GetData()
            
            npItems = []
            rItem = self.pnlRight.tc.GetRootItem()
            for item in self.pnlRight.tc.GetItemChildren( rItem, True ):
                attrib = item.GetData().getAttrib( pm.LightAttrib )
                if attrib is not None and light in attrib.getOnLights():
                    npItems.append( item )
                    
            self.pnlRight.SelectItems( npItems )
        
        self.pnlLeft.tc.Thaw()
        
    def OnRightTreeSelChanged( self, evt ):
        """
        Set relationship with those items selected in the left list with those
        the user has selected in the right list.
        """
        # Get the light NodePath selected in the left panel
        items = self.pnlLeft.GetValidSelections()
        if not items:
            self.pnlRight.tc.UnselectAll()
            return
        lgtNp = items[0].GetData()
        
        # Get the light attribute for the NodePath. Create an empty one if 
        # None is returned (has not had any lights applied yet).
        item = evt.GetItem()
        np = item.GetData()
        attrib = np.getAttrib( pm.LightAttrib )
        if attrib is None:
            
            # Set an empty light attrib so this works with the undo system.
            attrib = pm.LightAttrib.make()
            np.setAttrib( attrib )
        
        # Add / remove lights from the attrib.
        if item in self.pnlRight.tc.GetSelections():
            attrib = attrib.addOnLight( lgtNp )
        else:
            attrib = attrib.removeOnLight( lgtNp )
        
        # Construct the attribute and set it.
        attr = Attr( 'OnLight', pm.LightAttrib, NP.getAttrib, 
                     NP.setAttrib, getArgs=[pm.LightAttrib] )
        cmds.SetAttribute( [np], attr, attrib )