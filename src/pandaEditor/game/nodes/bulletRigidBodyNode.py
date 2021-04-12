import panda3d.core as pm
from panda3d.bullet import BulletRigidBodyNode as BRBN, BulletShape as BS

from game.nodes.manager import import_wrapper


NodePath = import_wrapper('nodes.nodePath.NodePath')
Attr = import_wrapper('nodes.attributes.Attribute')
NodeAttr = import_wrapper('nodes.attributes.NodeAttribute')
Cnnctn = import_wrapper('nodes.attributes.NodePathSourceConnection')


class BulletRigidBodyNode(NodePath):
    
    type_ = BRBN
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.AddAttributes(
            NodeAttr('Angular Damping', float, BRBN.getAngularDamping, BRBN.setAngularDamping),
            NodeAttr('Gravity', pm.Vec3, BRBN.getGravity, BRBN.setGravity),
            NodeAttr('Mass', float, BRBN.getMass, BRBN.setMass),
            Cnnctn('Shapes', BS, BRBN.getShapes, BRBN.addShape, self.ClearShapes, BRBN.removeShape, self.data),
            parent='BulletRigidBodyNode'
        )
        
    def ClearShapes(self, comp):
        numShapes = comp.getNumShapes()
        for i in range(numShapes):
            shape = comp.getShape(0)
            comp.removeShape(shape)