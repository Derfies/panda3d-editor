import os

import wx
import wx.lib.agw.floatspin as fs
import pandac.PandaModules as pm
from panda3d.core import Filename

#from propertiesPanel import ATTRIBUTE_TAG
from wxExtra import wxpg, CompositeDropTarget


class Float3Property( wxpg.BaseProperty ):
    
    def __init__( self, *args, **kwargs ):
        wxpg.BaseProperty.__init__( self, *args, **kwargs )
        
        self._ctrls = []
        self._count = 3
        self._cast = pm.Vec3 # HAXXOR
        
    def BuildControl( self, parent, id ):
        ctrl = wx.BoxSizer( wx.HORIZONTAL )
        for i in range( self._count ):
            spin = fs.FloatSpin( parent, id, value=self._value[i], digits=3 )
            spin.Enable( self.IsEnabled() )
            spin.Bind( fs.EVT_FLOATSPIN, self.OnChanged )
            ctrl.Add( spin, 1, wx.EXPAND )
            self._ctrls.append( spin )
        
        return ctrl
    
    def SetValueFromEvent( self, evt ):
        ctrl = evt.GetEventObject()
        index = self._ctrls.index( ctrl )
        self._value = self._cast( self._value )
        self._value[index] = ctrl.GetValue()
        

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
        

"""
class AnimationDictProperty( wxpg.PyStringProperty ):
    
    def __init__( self, *args, **kwargs ):
        self.animDict = kwargs.pop( 'attr' )
        wxpg.PyStringProperty.__init__( self, *args, **kwargs )
        
        for animName, animPath in self.animDict.items():
            self.AddPrivateChild( wxpg.FileProperty( animName, wxpg.LABEL_AS_NAME, str( animPath ) ) )
            
    def GetValueAsString( self, argFlags ):
        return ', '.join( self.animDict.keys() )
"""


class NodePathProperty( wxpg.StringProperty ):
    
    def BuildControl( self, parent, id ):
        np = self.GetValue()
        text = ''
        if np is not None:
            text = np.getName()
        
        ctrl = wx.TextCtrl( parent, id, value=text )
        ctrl.Bind( wx.EVT_TEXT, self.OnChanged )
        
        dt = CompositeDropTarget( ['nodePath', 'filePath'], 
                                  self.OnDropItem, 
                                  self.ValidateDropItem )
        ctrl.SetDropTarget( dt )
        
        return ctrl
    
    def ValidateDropItem( self, x, y ):
        return True
    
    def OnDropItem( self, arg ):
        np = wx.GetApp().frame.pnlSceneGraph.dragNps[0]
        self.SetValue( np )
        
        self.PostChangedEvent()
        

class ConnectionBaseProperty( wxpg.BaseProperty ):
    
    def BuildControl( self, parent, id ):
        ctrl = wx.ListBox( parent, id, size=(-1,50), style=wx.LB_EXTENDED )
        ctrl.Enable( self.IsEnabled() )
        ctrl.Bind( wx.EVT_KEY_UP, self.OnDelete )
        
        dt = CompositeDropTarget( ['nodePath'], 
                                  self.OnDropItem, 
                                  self.ValidateDropItem )
        ctrl.SetDropTarget( dt )
        
        return ctrl
    
    def ValidateDropItem( self, x, y ):
        for comp in wx.GetApp().frame.pnlSceneGraph.dragNps:
            cnnctn = self.GetAttribute( 'attr' )
            wrpr = base.game.nodeMgr.Wrap( comp )
            if wrpr.IsOfType( cnnctn.type ):
                return True
        
        return False
    

class ConnectionProperty( ConnectionBaseProperty ):
    
    def BuildControl( self, parent, id ):
        ctrl = ConnectionBaseProperty.BuildControl( self, parent, id )
        
        comp = self.GetValue()
        if comp is not None:
            wrpr = base.game.nodeMgr.Wrap( comp )
            ctrl.Append( wrpr.GetName() )
            ctrl.SetClientData( 0, wrpr.data )
        
        return ctrl
        
    def OnDelete( self, evt ):
        if evt.GetKeyCode() not in [wx.WXK_DELETE, wx.WXK_BACK]:
            return
        
        self.SetValue( None )
        self.PostChangedEvent()
    
    def OnDropItem( self, arg ):
        val = wx.GetApp().frame.pnlSceneGraph.dragNps[0]
        self.SetValue( val )
        self.PostChangedEvent()
        

class ConnectionListProperty( ConnectionBaseProperty ):
    
    def BuildControl( self, parent, id ):
        ctrl = ConnectionBaseProperty.BuildControl( self, parent, id )
        
        comps = self.GetValue()
        if comps is not None:
            for i in range( len( comps ) ):
                wrpr = base.game.nodeMgr.Wrap( comps[i] )
                ctrl.Append( wrpr.GetName() )
                ctrl.SetClientData( i, wrpr.data )
        
        return ctrl
    
    def OnDelete( self, evt ):
        """
        Remove those components that were selected in the list box from this
        property's value.
        """
        if evt.GetKeyCode() not in [wx.WXK_DELETE, wx.WXK_BACK]:
            return
        
        lb = evt.GetEventObject()
        indices = lb.GetSelections()
        delComps = [lb.GetClientData( i ) for i in range( len( indices ) )]
        oldComps = self.GetValue()
        newComps = [comp for comp in oldComps if comp not in delComps]
        self.SetValue( newComps )
        self.PostChangedEvent()
    
    def OnDropItem( self, arg ):
        val = self.GetValue()
        if val is None:
            val = []
        val.extend( wx.GetApp().frame.pnlSceneGraph.dragNps )
        self.SetValue( val )
        self.PostChangedEvent()
        

class DictProperty( wxpg.BaseProperty ):
    
    def BuildControl( self, parent, id ):
        ctrl = wx.ListBox( parent, id, size=(-1,50), style=wx.LB_EXTENDED )
        ctrl.Enable( self.IsEnabled() )
        ctrl.Bind( wx.EVT_KEY_UP, self.OnDelete )
        
        dt = CompositeDropTarget( ['filePath'], 
                                  self.OnDropItem, 
                                  self.ValidateDropItem )
        ctrl.SetDropTarget( dt )

        for name in self.GetValue():
            ctrl.Append( name )
        
        return ctrl
    
    def ValidateDropItem( self, x, y ):
        return True
    
    def OnDelete( self, evt ):
        pass
    
    def OnDropItem( self, arg ):
        myDict = dict( self.GetValue() )
        key = os.path.split( arg )[-1].split( '.' )[0]
        myDict[key] = arg
        self.SetValue( myDict )
        self.PostChangedEvent()