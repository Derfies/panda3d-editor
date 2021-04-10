import os

import wx
import wx.lib.mixins.listctrl as listmix
import panda3d.core as pm
from panda3d.core import Filename

from wxExtra import wxpg, CompositeDropTarget, utils as wxUtils
from wxExtra import CustomListCtrl
    

class Float3Property( wxpg.BaseProperty ):
    
    def __init__( self, *args, **kwargs ):
        wxpg.BaseProperty.__init__( self, *args, **kwargs )
        
        self._count = 3
        self._cast = pm.Vec3 # HAXXOR
        
    def BuildControl( self, parent ):
        bs = wx.BoxSizer( wx.HORIZONTAL )
        for i in range( self._count ):
            ctrl = wx.TextCtrl( parent, i, validator=wxpg.FloatValidator() )
            self.AppendControl( ctrl )
            bs.Add( ctrl, 1, wx.EXPAND )
        self.SetValue( self._value )
        return bs
    
    def SetValue( self, val ):
        wxpg.BaseProperty.SetValue( self, val )
        
        for i, ctrl in enumerate( self.GetControls() ):
            rndVal = round( val[i], 3 )
            ctrl.SetValue( str( rndVal ) )
    
    def SetValueFromEvent( self, evt ):
        self._value = self._cast( self._value )
        ctrl = evt.GetEventObject()
        index = ctrl.GetId()
        try:
            val = float( ctrl.GetValue() )
        except ValueError:
            val = 0
        self._value[index] = val
        

class Float2Property( Float3Property ):
    
    def __init__( self, *args, **kwargs ):
        Float3Property.__init__( self, *args, **kwargs )
        
        self._count = 2
        self._cast = pm.Vec2
        

class Float4Property( Float3Property ):
    
    def __init__( self, *args, **kwargs ):
        Float3Property.__init__( self, *args, **kwargs )
        
        self._count = 4
        self._cast = pm.Vec4
        

class Point2Property( Float3Property ):
    
    def __init__( self, *args, **kwargs ):
        Float3Property.__init__( self, *args, **kwargs )
        
        self._count = 2
        self._cast = pm.Point2
        

class Point3Property( Float3Property ):
    
    def __init__( self, *args, **kwargs ):
        Float3Property.__init__( self, *args, **kwargs )
        
        self._count = 3
        self._cast = pm.Point3
        

class Point4Property( Float3Property ):
    
    def __init__( self, *args, **kwargs ):
        Float3Property.__init__( self, *args, **kwargs )
        
        self._count = 4
        self._cast = pm.Point4
        
        
class FilePathProperty( wxpg.StringProperty ):
    
    def SetValueFromEvent( self, evt ):
        ctrl = evt.GetEventObject()
        val = ctrl.GetValue()
        self.SetValue( Filename.fromOsSpecific( val ) )
        
    def BuildControl( self, *args, **kwargs ):
        ctrl = wxpg.StringProperty.BuildControl( self, *args, **kwargs )
        dt = CompositeDropTarget( ['filePath'], self.OnDropItem, self.ValidateDropItem )
        ctrl.SetDropTarget( dt )
        return ctrl
    
    def OnDropItem( self, arg ):
        self.SetValue( arg )
        self.PostChangedEvent()
        
    def ValidateDropItem( self, *args ):
        return True
    

class NodePathProperty( wxpg.StringProperty ):
    
    def BuildControl( self, parent ):
        np = self.GetValue()
        text = ''
        if np is not None:
            text = np.getName()
        
        ctrl = wx.TextCtrl( parent, -1, value=text )
        ctrl.Bind( wx.EVT_TEXT, self.OnChanged )
        
        dt = CompositeDropTarget( ['nodePath', 'filePath'], 
                                  self.OnDropItem, 
                                  self.ValidateDropItem )
        ctrl.SetDropTarget( dt )
        
        return ctrl
    
    def ValidateDropItem( self, x, y ):
        return True
    
    def OnDropItem( self, arg ):
        np = wx.GetApp().frame.pnlSceneGraph.dragComps[0]
        self.SetValue( np )
        
        self.PostChangedEvent()
        

class ConnectionBaseProperty( wxpg.BaseProperty ):
    
    def BuildControl( self, parent, height ):
        ctrl = wx.ListBox( parent, -1, size=wx.Size( -1, height ), style=wx.LB_EXTENDED )
        ctrl.Enable( self.IsEnabled() )
        ctrl.Bind( wx.EVT_KEY_UP, self.OnKeyUp )
        
        dt = CompositeDropTarget( ['nodePath'], 
                                  self.OnDropItem, 
                                  self.ValidateDropItem )
        ctrl.SetDropTarget( dt )
        
        return ctrl
    
    def OnKeyUp( self, evt ):
        pass
    
    def ValidateDropItem( self, x, y ):
        for comp in wx.GetApp().frame.pnlSceneGraph.dragComps:
            cnnctn = self.GetAttribute( 'attr' )[0]
            wrpr = base.game.nodeMgr.Wrap( comp )
            if wrpr.IsOfType( cnnctn.type ):
                return True
        
        return False
    

class ConnectionProperty( ConnectionBaseProperty ):
    
    def BuildControl( self, parent ):
        height = parent.GetSize()[1]
        ctrl = ConnectionBaseProperty.BuildControl( self, parent, height )
        
        comp = self.GetValue()
        if comp is not None:
            wrpr = base.game.nodeMgr.Wrap( comp )
            ctrl.Append( wrpr.GetName() )
            ctrl.SetClientData( 0, wrpr.data )
        
        return ctrl
        
    def OnKeyUp( self, evt ):
        if evt.GetKeyCode() not in [wx.WXK_DELETE, wx.WXK_BACK]:
            return
        
        self.SetValue( None )
        self.PostChangedEvent()
    
    def OnDropItem( self, arg ):
        val = wx.GetApp().frame.pnlSceneGraph.dragComps[0]
        self.SetValue( val )
        self.PostChangedEvent()
        

class ConnectionListProperty( ConnectionBaseProperty ):
    
    def BuildControl( self, parent ):
        ctrl = ConnectionBaseProperty.BuildControl( self, parent, -1 )
        
        comps = self.GetValue()
        if comps is not None:
            for i in range( len( comps ) ):
                wrpr = base.game.nodeMgr.Wrap( comps[i] )
                ctrl.Append( wrpr.GetName(), wrpr.data )
        
        return ctrl
    
    def OnKeyUp( self, evt ):
        """
        Remove those components that were selected in the list box from this
        property's value.
        """
        if evt.GetKeyCode() not in [wx.WXK_DELETE, wx.WXK_BACK]:
            return
        
        lb = evt.GetEventObject()
        delComps = [lb.GetClientData( index ) for index in lb.GetSelections()]
        oldComps = self.GetValue()
        newComps = [comp for comp in oldComps if comp not in delComps]
        self.SetValue( newComps )
        self.PostChangedEvent()
    
    def OnDropItem( self, arg ):
        val = self.GetValue()
        if val is None:
            val = []
        val.extend( wx.GetApp().frame.pnlSceneGraph.dragComps )
        self.SetValue( val )
        self.PostChangedEvent()
        

class DictProperty( wxpg.BaseProperty ):
    
    def BuildControl( self, parent ):
        ctrl = CustomListCtrl( parent, -1, style=wx.LC_REPORT | wx.LC_EDIT_LABELS )
        ctrl.InsertColumn( 0, 'Name' )
        ctrl.InsertColumn( 1, 'Value' )
        ctrl.Enable( self.IsEnabled() )
        ctrl.Bind( wx.EVT_KEY_UP, self.OnKeyUp )
        ctrl.Bind( wx.EVT_LIST_END_LABEL_EDIT, self.OnListEndLabelEdit )
        
        dt = CompositeDropTarget( ['nodePath'], 
                                  self.OnDropItem, 
                                  self.ValidateDropItem )
        ctrl.SetDropTarget( dt )

        for key, val in self.GetValue().items():
            ctrl.InsertStringItem( 0, str( key ) )
            ctrl.SetStringItem( 0, 1, str( val ) )
        
        return ctrl
    
    def ValidateDropItem( self, x, y ):
        return True
    
    def OnKeyUp( self, evt ):
        if evt.GetKeyCode() not in [wx.WXK_DELETE, wx.WXK_BACK]:
            return
        
        # Get the names of the items selected, then remove these keys from 
        # the dictionary.
        ctrl = evt.GetEventObject()
        keys = [item.GetText() for item in ctrl.GetAllItems()]
        myDict = dict( self.GetValue() )
        for index in ctrl.GetSelections():
            del myDict[keys[index]]
        
        self.SetValue( myDict )
        self.PostChangedEvent()
    
    def OnDropItem( self, arg ):
        myDict = dict( self.GetValue() )
        key = os.path.split( arg )[-1].split( '.' )[0]
        myDict[key] = arg
        self.SetValue( myDict )
        self.PostChangedEvent()
        
    def OnListEndLabelEdit( self, evt ):
        
        item = evt.GetItem()
        ctrl = evt.GetEventObject()
        oldKey = ctrl.GetItem( item.GetId() ).GetText()
        newKey = item.GetText()
        
        pDict = self.GetValue()
        val = pDict.pop( oldKey )
        pDict[newKey] = val
        self.SetValue( pDict )
        self.PostChangedEvent()