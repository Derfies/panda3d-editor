import pandac.PandaModules as pm
from panda3d.bullet import BulletCharacterControllerNode as BCCN, BulletShape as BS

from nodePath import NodePath
from attributes import NodeAttribute as Attr
from game.nodes.connections import NodePathSourceConnectionList as Cnnctn


class BulletCharacterControllerNode( NodePath ):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'cType', BCCN )
        NodePath.__init__( self, *args, **kwargs )
        
        pAttr = Attr( 'BulletCharacterControllerNode' )
        pAttr.children.extend( 
            [
                #Attr( 'Angular Damping', float, BRBN.getAngularDamping, BRBN.setAngularDamping ),
                #Attr( 'Gravity', pm.Vec3, BRBN.getGravity, BRBN.setGravity ),
                #Attr( 'Mass', float, BRBN.getMass, BRBN.setMass ),
                #Cnnctn( 'Shape', BS, BRBN.getShapes, BRBN.addShape, self.ClearShapes, BRBN.removeShape, self.data )
            ]
        )
        self.attributes.append( pAttr )
        
    #def ClearShapes( self, comp ):
    #    numShapes = comp.getNumShapes()
    #    for i in range( numShapes ):
    #        shape = comp.getShape( 0 )
    #        comp.removeShape( shape )