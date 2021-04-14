import panda3d.core as pc

from game.nodes.attributes import (
    Attribute,
    NodeAttribute,
    NodePathSourceConnectionList
)
from game.nodes.base import Base
from game.nodes.nodepath import NodePath


class CollisionNode(NodePath):
    
    type_ = pc.CollisionNode
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.AddAttributes(
            NodeAttribute('Num Solids', int, pc.CollisionNode.get_num_solids),
            NodePathSourceConnectionList(
                'Solids',
                pc.CollisionSolid,
                pc.CollisionNode.get_solids,
                pc.CollisionNode.add_solid,
                pc.CollisionNode.clear_solids,
                self.RemoveSolid,
                self.data
            ),
            parent='CollisionNode'
       )
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = super().Create(*args, **kwargs)
        wrpr.data.show()
        return wrpr
    
    def RemoveSolid(self, srcComp, tgtComp):
        solids = srcComp.getSolids()
        index = solids.index(tgtComp)
        CollisionNode.removeSolid(srcComp, index)


class CollisionBox(Base):
    
    type_ = pc.CollisionBox

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            Attribute('X', float, initDefault=0.5),
            Attribute('Y', float, initDefault=0.5),
            Attribute('Z', float, initDefault=0.5),
            Attribute('Center', pc.Point3, pc.CollisionBox.getCenter, pc.CollisionBox.setCenter,
                 initDefault=pc.Point3(0)),
            parent='CollisionBox'
        )


class CollisionRay(Base):
    
    type_ = pc.CollisionRay

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            Attribute('Origin', pc.Point3, pc.CollisionRay.getOrigin, pc.CollisionRay.setOrigin,
                 initDefault=pc.Point3(0)),
            Attribute('Direction', pc.Vec3, pc.CollisionRay.getDirection, pc.CollisionRay.setDirection,
                 initDefault=pc.Vec3(0, 0, 1)),
            parent='CollisionRay'
        )


class CollisionSphere(Base):
    
    type_ = pc.CollisionSphere

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            Attribute('Center', pc.Point3, pc.CollisionSphere.getCenter, pc.CollisionSphere.setCenter,
                 initDefault=pc.Point3(0)),
            Attribute('Radius', float, pc.CollisionSphere.getRadius, pc.CollisionSphere.setRadius,
                 initDefault=0.5),
            parent='CollisionSphere'
        )


class CollisionInvSphere(CollisionSphere):
    
    type_ = pc.CollisionInvSphere


class CollisionTube(Base):
    
    type_ = pc.CollisionTube

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            Attribute('Point A', pc.Point3, pc.CollisionTube.getPointA, pc.CollisionTube.setPointA,
                 initDefault=pc.Point3(0), initName='a'),
            Attribute('Point B', pc.Point3, pc.CollisionTube.getPointB, pc.CollisionTube.setPointB,
                 initDefault=pc.Point3(0, 0, 1), initName='db'),
            Attribute('Radius', float, pc.CollisionTube.getRadius, pc.CollisionTube.setRadius,
                 initDefault=0.5),
            parent='CollisionTube'
        )
