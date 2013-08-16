import pandac.PandaModules as pm

import p3d
import game
from constants import *
from primitive import Primitive, PrimitiveNPO
from game.nodes.attributes import NodePathObjectAttribute as NPOAttr


class CylinderNPO( PrimitiveNPO ):
    
    radius = property( PrimitiveNPO.attrgetter( '_radius' ), 
                       PrimitiveNPO.attrsetter( '_radius' ) )
    height = property( PrimitiveNPO.attrgetter( '_height' ), 
                       PrimitiveNPO.attrsetter( '_height' ) )
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
        self._height = 2
        self._numSegs = 16
        self._degrees = 360
        self._axis = pm.Vec3(0, 0, 1)
        self._origin = pm.Point3(0, 0, 0)
        
    def Rebuild( self ):
        """Rebulid the cylinder and update geoms."""
        self.np.node().removeAllGeoms()
        cylinderGeom = p3d.geometry.Cylinder( self._radius, self._height, 
                                              self._numSegs, self._degrees, 
                                              self._axis, self._origin )
        self.np.node().addGeomsFrom( cylinderGeom )
    

class Cylinder( Primitive ):
    
    def __init__( self, *args, **kwargs ):
        Primitive.__init__( self, *args, **kwargs )
        
        datas = (
            ('Radius', float, 'radius'),
            ('Height', float, 'height'),
            ('NumSegs', int, 'numSegs'),
            ('Degrees', int, 'degrees'),
            ('Axis', pm.Vec3, 'axis'),
            ('Origin', pm.Point3, 'origin' ),
        )
        for data in datas:
            self.AddAttributes( NPOAttr( *data, pyTagName=TAG_PRIMITIVE_OBJECT ), parent='Cylinder' )
        
    def SetupNodePath( self ):
        Primitive.SetupNodePath( self )
        
        self.data.setName( 'cylinder' )
        self.data.setTag( game.nodes.TAG_NODE_TYPE, TAG_CYLINDER )
        CylinderNPO( self.data )
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        wrpr = cls( pm.NodePath( p3d.geometry.Cylinder() ) )
        wrpr.SetupNodePath()
        return wrpr