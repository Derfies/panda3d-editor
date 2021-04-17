import panda3d.core as pm
from panda3d.bullet import BulletBoxShape as BBS
from panda3d.bullet import BulletCapsuleShape as BCS
from panda3d.bullet import BulletWorld as BW
from panda3d.bullet import BulletDebugNode as BDN
from panda3d.bullet import BulletCharacterControllerNode as BCCN
from panda3d.bullet import BulletPlaneShape as BPS
from panda3d.bullet import BulletRigidBodyNode as BRBN, BulletShape as BS
from panda3d.bullet import ZUp

from game.nodes.attributes import (
    Attribute,
    #Connection,
    ConnectionList,
    NodeAttribute,
    NodePathSourceConnectionList,
    NodePathTargetConnection,
    NodePathTargetConnectionList,
)
from game.nodes.base import Base
from game.nodes.nodepath import NodePath


TAG_BULLET_DEBUG_WIREFRAME = 'P3D_BulletDebugWireframe'


class BulletBoxShape(Base):

    type_ = BBS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            Attribute('Half Extents', pm.Vec3, BBS.getHalfExtentsWithMargin,
                 init_arg=pm.Vec3(0.5, 0.5, 0.5)),
            parent='BulletBoxShape'
        )


class BulletCapsuleShape(Base):

    type_ = BCS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            Attribute('Radius', float, BCS.getRadius, init_arg=0.5),
            Attribute('Height', float, BCS.getHalfHeight, init_arg=1),
            Attribute('Up', int, init_arg=ZUp),
            parent='BulletCapsuleShape'
        )


class BulletCharacterControllerNode(NodePath):

    type_ = BCCN

    def __init__(self, *args, **kwargs):
        NodePath.__init__(self, *args, **kwargs)

        self.AddAttributes(
            Attribute('Shape', BCS, init_arg=BCS(0.4, 1.75 - 2 * 0.4, ZUp)),
            Attribute('step_height', float, init_arg=0.4),
            Attribute('Name', str),
            parent='BulletCharacterControllerNode'
        )


class BulletDebugNode(NodePath):

    type_ = BDN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            Attribute('Show Wireframe', bool, self.GetWireframe, self.SetWireframe),
            parent='BulletDebugNode'
        )

    @classmethod
    def create(cls, *args, **kwargs):
        wrpr = super(BulletDebugNode, cls).create(*args, **kwargs)
        wrpr.SetWireframe(wrpr.data, True)
        wrpr.data.show()
        return wrpr

    def GetWireframe(self, np):
        return np.getPythonTag(TAG_BULLET_DEBUG_WIREFRAME)

    def SetWireframe(self, np, val):
        np.node().showWireframe(val)
        np.setPythonTag(TAG_BULLET_DEBUG_WIREFRAME, val)


class BulletPlaneShape(Base):

    type_ = BPS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            Attribute('Normal', pm.Vec3, init_arg=pm.Vec3(0, 0, 1)),
            Attribute('Constant', int, init_arg=0),
            parent='BulletBoxShape'
        )


class BulletRigidBodyNode(NodePath):

    type_ = BRBN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            NodeAttribute('Angular Damping', float, BRBN.getAngularDamping, BRBN.setAngularDamping),
            NodeAttribute('Gravity', pm.Vec3, BRBN.getGravity, BRBN.setGravity),
            NodeAttribute('Mass', float, BRBN.getMass, BRBN.setMass),
            NodePathSourceConnectionList ('Shapes', BS, BRBN.getShapes, BRBN.addShape, self.ClearShapes, BRBN.removeShape, self.data),
            parent='BulletRigidBodyNode'
        )

    def ClearShapes(self, comp):
        numShapes = comp.getNumShapes()
        for i in range(numShapes):
            shape = comp.getShape(0)
            comp.removeShape(shape)


class BulletWorld(Base):

    type_ = BW

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            Attribute('Gravity', pm.Vec3, BW.getGravity, BW.setGravity),
            NodePathTargetConnectionList('Rigid Body', BRBN, BW.getRigidBodies, BW.attachRigidBody, self.ClearRigidBodies,
                       BW.removeRigidBody, self.data),
            NodePathTargetConnectionList('Character', BCCN, BW.getCharacters, BW.attachCharacter, self.ClearCharacters,
                       BW.removeCharacter, self.data),
            NodePathTargetConnection('Debug Node', BDN, self.GetDebugNode, BW.setDebugNode, BW.clearDebugNode, self.data),
            parent='BulletWorld'
        )

    def destroy(self):
        if (
            base.scene.physics_world is self.data and
            base.scene.physics_task in taskMgr.getAllTasks()
        ):
            self.DisablePhysics()

    def ClearRigidBodies(self, comp):
        for i in range(comp.getNumRigidBodies()):
            comp.removeRigidBody(comp.getRigidBody(0))

    def ClearCharacters(self, comp):
        for i in range(comp.getNumCharacters()):
            comp.removeCharacter(comp.getCharacter(0))

    def GetDebugNode(self, args):
        pass

    def EnablePhysics(self):

        def update(task):
            dt = globalClock.getDt()
            self.data.doPhysics(dt)
            return task.cont

        base.scene.physics_task = taskMgr.add(update, 'update')

    def DisablePhysics(self):
        taskMgr.remove(base.scene.physics_task)
