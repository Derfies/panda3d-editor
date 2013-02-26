import p3d
import game
from script import Script
from game.nodes.base import Base
from game.nodes import Attribute as Attr


class PandaObject( Base ):
        
    def Create( self, *args, **kwargs ):
        self.data = p3d.PandaObject()
        return self.data
    
    def Destroy( self ):
        p3d.PandaObject.Break( self.data.np )
        self.data = None
    
    def GetAttributes( self, flat=None, addons=None ):
        attrs = []
        for name, instance in self.data.instances.items():
            pAttr = Attr( name )
            for pName, pType in self.GetProps( instance ).items():
                pAttr.children.append( Attr( pName, pType, getattr, setattr, self.GetPObjInstance, [pName], [pName], [name], w=False ) )
            attrs.append( pAttr )
        
        return attrs
    
    def GetPObjInstance( self, np, clsName ):
        return p3d.PandaObject.Get( np ).instances[clsName]
    
    def GetProps( self, instance ):
        props = {}
        for pName, prop in vars( instance.__class__ ).items():
            if type( prop ) == type:
                props[pName] = prop
                
        return props
    
    def GetChildren( self ):
        children = []
        
        # Create wrappers for each script attached to the object.
        for name, instance in self.data.instances.items():
            children.append( Script( instance ) )
            
        return children
    
    def SetParent( self, pNp ):
        self.data.AttachToNodePath( pNp )
        
        pyTag = pNp.getPythonTag( game.nodes.TAG_PYTHON_TAGS )
        if pyTag is None:
            pyTag = []
            pNp.setPythonTag( game.nodes.TAG_PYTHON_TAGS, pyTag )
            
        if p3d.TAG_PANDA_OBJECT not in pyTag:
            pyTag.append( p3d.TAG_PANDA_OBJECT )
        
    def GetEveryAttribute( self ):
        return self.GetAllAttributes()