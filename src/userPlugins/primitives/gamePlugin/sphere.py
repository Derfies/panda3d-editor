import pandac.PandaModules as pm

import p3d
import game
from constants import *
from primitive import Primitive, PrimitiveNPO
from game.nodes import NodePathObjectAttribute as NPOAttr


class SphereNPO( PrimitiveNPO ):
        
    radius = property( PrimitiveNPO.attrgetter( '_radius' ), 
                       PrimitiveNPO.attrsetter( '_radius' ) )
    numSegs = property( PrimitiveNPO.attrgetter( '_numSegs' ), 
                        PrimitiveNPO.attrsetter( '_numSegs' ) )
    degrees = property( PrimitiveNPO.attrgetter( '_degrees' ), 
                        PrimitiveNPO.attrsetter( '_degrees' ) )
    axis = property( PrimitiveNPO.attrgetter( '_axis' ), 
                     PrimitiveNPO.attrsetter( '_axis' ) )
    origin = property( PrimitiveNPO.attrgetter( '_origin' ), 
                       PrimitiveNPO.attrsetter( '_origin' ) )
                       
    def __init__( self, *args, **kwargs ):
        PrimitiveNPO.__init__( self, *args, **kwargs )
        
        self._radius = 1
        self._numSegs = 16
        self._degrees = 360
        self._axis = pm.Vec3(0, 0, 1)
        self._origin = pm.Point3(0, 0, 0)
    
    def Rebuild( self ):
        """Rebulid the sphere and update geoms."""
        self.np.node().removeAllGeoms()
        sphereGeom = p3d.geometry.Sphere( self._radius, self._numSegs, 
                                          self._degrees, self._axis, 
                                          self._origin )
        self.np.node().addGeomsFrom( sphereGeom )
    

class Sphere( Primitive ):
    
    def __init__( self, *args, **kwargs ):
        Primitive.__init__( self, *args, **kwargs )
        
        datas = (
            ('Radius', float, 'radius'),
            ('NumSegs', int, 'numSegs'),
            ('Degrees', int, 'degrees'),
            ('Axis', pm.Vec3, 'axis'),
            ('Origin', pm.Point3, 'origin')
        )
        for data in datas:
            self.AddAttributes( NPOAttr( *data, pyTagName=TAG_PRIMITIVE_OBJECT ), parent='Sphere' )
        
    def SetupNodePath( self ):
        Primitive.SetupNodePath( self )
        
        self.data.setName( 'sphere' )
        self.data.setTag( game.nodes.TAG_NODE_TYPE, TAG_SPHERE )
        SphereNPO( self.data )
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        wrpr = cls( pm.NodePath( p3d.geometry.Sphere() ) )
        wrpr.SetupNodePath()
        return wrpr