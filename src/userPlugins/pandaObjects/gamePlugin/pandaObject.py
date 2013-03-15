import p3d
import game
from game.nodes.base import Base
from game.nodes import Attribute as Attr


class PandaObject( Base ):
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        return cls( p3d.PandaObject() )
    
    def Detach( self ):
        
        # Remove the NodePath's tag referencing the PandaObject. Also remove
        # the PandaObject tag from the list of tags on this NodePath.
        self.data.np.clearPythonTag( p3d.TAG_PANDA_OBJECT )
        pyTag = self.data.np.getPythonTag( game.nodes.TAG_PYTHON_TAGS )
        if pyTag is not None:
            pyTag.remove( p3d.TAG_PANDA_OBJECT )
    
    def Destroy( self ):
        p3d.PandaObject.Break( self.data.np )
        self.data = None
    
    def GetAttributes( self, *args, **kwargs ):
        attrs = []
        for name, instance in self.data.instances.items():
            for pName, pType in self.GetProps( instance ).items():
                attrs.append( Attr( pName, pType, getattr, setattr, self.GetPObjInstance, [pName], [pName], [name], w=False, parent=name,srcComp=self.data ) )
        
        return attrs
    
    def GetPObjInstance( self, pObj, clsName ):
        return pObj.instances[clsName]
    
    def GetProps( self, instance ):
        props = {}
        for pName, prop in vars( instance.__class__ ).items():
            if type( prop ) == type:
                props[pName] = prop
                
        return props
    
    def GetChildren( self ):
        children = []
        
        # Create wrappers for each script attached to the object.
        wrprCls = base.game.nodeMgr.nodeWrappers['Script']
        for name, instance in self.data.instances.items():
            children.append( wrprCls( instance ) )
            
        return children
    
    def GetParent( self ):
        return self.data.np
    
    def SetParent( self, pNp ):
        if pNp is None:
            return
        
        self.data.AttachToNodePath( pNp )
        
        pyTag = pNp.getPythonTag( game.nodes.TAG_PYTHON_TAGS )
        if pyTag is None:
            pyTag = []
            pNp.setPythonTag( game.nodes.TAG_PYTHON_TAGS, pyTag )
            
        if p3d.TAG_PANDA_OBJECT not in pyTag:
            pyTag.append( p3d.TAG_PANDA_OBJECT )
        
    def GetEveryAttribute( self ):
        return self.GetAllAttributes()