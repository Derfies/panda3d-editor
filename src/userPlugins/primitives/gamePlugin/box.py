import panda3d.core as pm

import p3d
import game
from .constants import *
from primitive import Primitive, PrimitiveNPO
from game.nodes.attributes import NodePathObjectAttribute as NPOAttr


class BoxNPO( PrimitiveNPO ):
    
    width = property( PrimitiveNPO.attrgetter( '_width' ), 
                      PrimitiveNPO.attrsetter( '_width' ) )
    depth = property( PrimitiveNPO.attrgetter( '_depth' ), 
                      PrimitiveNPO.attrsetter( '_depth' ) )
    height = property( PrimitiveNPO.attrgetter( '_height' ), 
                       PrimitiveNPO.attrsetter( '_height' ) )
    origin = property( PrimitiveNPO.attrgetter( '_origin' ), 
                       PrimitiveNPO.attrsetter( '_origin' ) )
    
    def __init__( self, *args, **kwargs ):
        PrimitiveNPO.__init__( self, *args, **kwargs )
        
        self._width = 1
        self._depth = 1
        self._height = 1
        self._origin = pm.Point3(0, 0, 0)
        
    def Rebuild( self ):
        """Rebulid the box and update geoms."""
        self.np.node().removeAllGeoms()
        boxGeom = p3d.geometry.Box( self._width, self._depth, self._height, 
                                    self._origin )
        self.np.node().addGeomsFrom( boxGeom )
    

class Box( Primitive ):
    
    def __init__( self, *args, **kwargs ):
        Primitive.__init__( self, *args, **kwargs )
        
        datas = (
            ('Width', float, 'width'),
            ('Depth', float, 'depth'),
            ('Height', float, 'height'),
            ('Origin', pm.Point3, 'origin')
        )
        for data in datas:
            self.AddAttributes( NPOAttr( *data, pyTagName=TAG_PRIMITIVE_OBJECT ), parent='Box' )
        
    def SetupNodePath( self ):
        Primitive.SetupNodePath( self )
        
        self.data.setName( 'box' )
        self.data.setTag( game.nodes.TAG_NODE_TYPE, TAG_BOX )
        BoxNPO( self.data )
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        wrpr = cls( pm.NodePath( p3d.geometry.Box() ) )
        wrpr.SetupNodePath()
        return wrpr