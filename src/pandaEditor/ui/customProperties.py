import wx
import wx.lib.agw.floatspin as fs
import pandac.PandaModules as pm

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
            spin = fs.FloatSpin( parent, id, value=self._value[i] )
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
        
        # Call after otherwise we crash!
        evt = wxpg.PropertyGridEvent( wxpg.wxEVT_PG_CHANGED )
        evt.SetProperty( self )
        fn = lambda event: self.GetGrid().GetEventHandler().ProcessEvent( evt )
        wx.CallAfter( fn )