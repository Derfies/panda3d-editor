import pandac.PandaModules as pm

import p3d
import game
from constants import *
from game.nodes.nodePath import NodePath
from game.nodes import Attribute as Attr
from game.nodes import NodePathObjectAttribute as NPOAttr


class SphereNPO( p3d.NodePathObject ):
    
    def __init__( self, *args, **kwargs ):
        p3d.NodePathObject.__init__( self, *args, **kwargs )
        
        self._radius = 1
        self._numSegs = 16
        self._degrees = 360
        self._axis = pm.Vec3(0, 0, 1)
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

    radius = property( attrgetter( '_radius' ), attrsetter( '_radius' ) )
    numSegs = property( attrgetter( '_numSegs' ), attrsetter( '_numSegs' ) )
    degrees = property( attrgetter( '_degrees' ), attrsetter( '_degrees' ) )
    axis = property( attrgetter( '_axis' ), attrsetter( '_axis' ) )
    origin = property( attrgetter( '_origin' ), attrsetter( '_origin' ) )
        
    def Rebuild( self ):
        """Rebulid the cone and update geoms."""
        self.np.node().removeAllGeoms()
        coneGeom = p3d.geometry.Sphere( self._radius, self._numSegs, 
                                        self._degrees, self._axis, 
                                        self._origin )
        self.np.node().addGeomsFrom( coneGeom )
    

class Sphere( NodePath ):
    
    def __init__( self, *args, **kwargs ):
        NodePath.__init__( self, *args, **kwargs )
        
        pAttr = Attr( 'Sphere' )
        pAttr.children.extend( 
            [
                NPOAttr( 'Radius', float, 'radius' ),
                NPOAttr( 'NumSegs', int, 'numSegs' ),
                NPOAttr( 'Degrees', int, 'degrees' ),
                NPOAttr( 'Axis', pm.Vec3, 'axis' ),
                NPOAttr( 'Origin', pm.Point3, 'origin' )
            ]
        )
        self.attributes.append( pAttr )
        
    def SetupNodePath( self, np ):
        NodePath.SetupNodePath( self, np )
        
        np.setName( 'sphere' )
        np.setTag( game.nodes.TAG_NODE_TYPE, TAG_SPHERE )
        SphereNPO( np )
    
    def Create( self ):
        np = pm.NodePath( p3d.geometry.Sphere() )
        self.SetupNodePath( np )
        self.data = np
        return np