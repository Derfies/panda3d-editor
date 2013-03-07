import pandac.PandaModules as pm

import p3d
import game
from constants import *
from game.nodes.nodePath import NodePath
from game.nodes import NodePathObjectAttribute as NPOAttr


class BoxNPO( p3d.NodePathObject ):
    
    def __init__( self, *args, **kwargs ):
        p3d.NodePathObject.__init__( self, *args, **kwargs )
        
        self._width = 1
        self._depth = 1
        self._height = 1
        self._origin = pm.Point3(0, 0, 0)
        
    def attrgetter( attr ):
        def get_any( self ):
            return getattr( self, attr )
        return get_any
        
    def attrsetter( attr ):
        def set_any( self, value ):
            setattr( self, attr, value )
            self.Rebuild()
        return set_any

    width = property( attrgetter( '_width' ), attrsetter( '_width' ) )
    depth = property( attrgetter( '_depth' ), attrsetter( '_depth' ) )
    height = property( attrgetter( '_height' ), attrsetter( '_height' ) )
    origin = property( attrgetter( '_origin' ), attrsetter( '_origin' ) )
        
    def Rebuild( self ):
        """Rebulid the box and update geoms."""
        self.np.node().removeAllGeoms()
        boxGeom = p3d.geometry.Box( self._width, self._depth, self._height, 
                                    self._origin )
        self.np.node().addGeomsFrom( boxGeom )
    

class Box( NodePath ):
    
    def __init__( self, *args, **kwargs ):
        NodePath.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            NPOAttr( 'Width', float, 'width' ),
            NPOAttr( 'Depth', float, 'depth' ),
            NPOAttr( 'Height', float, 'height' ),
            NPOAttr( 'Origin', pm.Point3, 'origin' ),
            parent='Box'
        )
    
    def SetupNodePath( self ):
        NodePath.SetupNodePath( self )
        
        self.data.setName( 'box' )
        self.data.setTag( game.nodes.TAG_NODE_TYPE, TAG_BOX )
        BoxNPO( self.data )
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        wrpr = cls( pm.NodePath( p3d.geometry.Box() ) )
        wrpr.SetupNodePath()
        return wrpr
    
    def Destroy( self ):
        p3d.NodePathObject.Break( self.data )
        NodePath.Destroy( self )