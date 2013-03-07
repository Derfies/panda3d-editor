import pandac.PandaModules as pm
from panda3d.bullet import BulletRigidBodyNode as BRBN, BulletShape as BS

from nodePath import NodePath
from attributes import NodeAttribute as Attr
from game.nodes.attributes import NodePathSourceConnectionList as Cnnctn


class BulletRigidBodyNode( NodePath ):
    
    type_ = BRBN
    
    def __init__( self, *args, **kwargs ):
        NodePath.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Angular Damping', float, BRBN.getAngularDamping, BRBN.setAngularDamping ),
            Attr( 'Gravity', pm.Vec3, BRBN.getGravity, BRBN.setGravity ),
            Attr( 'Mass', float, BRBN.getMass, BRBN.setMass ),
            Cnnctn( 'Shapes', BS, BRBN.getShapes, BRBN.addShape, self.ClearShapes, BRBN.removeShape, self.data ),
            parent='BulletRigidBodyNode'
        )
        
    def ClearShapes( self, comp ):
        numShapes = comp.getNumShapes()
        for i in range( numShapes ):
            shape = comp.getShape( 0 )
            comp.removeShape( shape )