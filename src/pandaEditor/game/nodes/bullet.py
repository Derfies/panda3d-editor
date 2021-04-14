import panda3d.core as pm
from panda3d.bullet import BulletBoxShape as BBS

from game.nodes.manager import import_wrapper

Base = import_wrapper('nodes.base.Base')
Attr = import_wrapper('nodes.attributes.Attribute')


class BulletBoxShape(Base):
    type_ = BBS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            Attr('Half Extents', pm.Vec3, BBS.getHalfExtentsWithMargin,
                 initDefault=pm.Vec3(0.5, 0.5, 0.5)),
            parent='BulletBoxShape'
        )


from panda3d.bullet import BulletCapsuleShape as BCS, ZUp

from game.nodes.manager import import_wrapper

Base = import_wrapper('nodes.base.Base')
Attr = import_wrapper('nodes.attributes.Attribute')


class BulletCapsuleShape(Base):
    type_ = BCS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            Attr('Radius', float, BCS.getRadius, initDefault=0.5),
            Attr('Height', float, BCS.getHalfHeight, initDefault=1),
            Attr('Up', int, initDefault=ZUp),
            parent='BulletCapsuleShape'
        )


from panda3d.bullet import ZUp
from panda3d.bullet import BulletCapsuleShape as BCS
from panda3d.bullet import BulletCharacterControllerNode as BCCN

from game.nodes.manager import import_wrapper

NodePath = import_wrapper('nodes.nodePath.NodePath')
Attr = import_wrapper('nodes.attributes.Attribute')


class BulletCharacterControllerNode(NodePath):
    type_ = BCCN

    def __init__(self, *args, **kwargs):
        NodePath.__init__(self, *args, **kwargs)

        self.AddAttributes(
            Attr('Shape', BCS, initDefault=BCS(0.4, 1.75 - 2 * 0.4, ZUp)),
            Attr('step_height', float, initDefault=0.4),
            Attr('Name', str),
            parent='BulletCharacterControllerNode'
        )


from panda3d.bullet import BulletDebugNode as BDN

from game.nodes.manager import import_wrapper

TAG_BULLET_DEBUG_WIREFRAME = 'P3D_BulletDebugWireframe'

NodePath = import_wrapper('nodes.nodePath.NodePath')
Attr = import_wrapper('nodes.attributes.Attribute')


class BulletDebugNode(NodePath):
    type_ = BDN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            Attr('Show Wireframe', bool, self.GetWireframe, self.SetWireframe),
            parent='BulletDebugNode'
        )

    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = super(BulletDebugNode, cls).Create(*args, **kwargs)
        wrpr.SetWireframe(wrpr.data, True)
        wrpr.data.show()
        return wrpr

    def GetWireframe(self, np):
        return np.getPythonTag(TAG_BULLET_DEBUG_WIREFRAME)

    def SetWireframe(self, np, val):
        np.node().showWireframe(val)
        np.setPythonTag(TAG_BULLET_DEBUG_WIREFRAME, val)


import panda3d.core as pm
from panda3d.bullet import BulletPlaneShape as BPS

from game.nodes.manager import import_wrapper

Base = import_wrapper('nodes.base.Base')
Attr = import_wrapper('nodes.attributes.Attribute')


class BulletPlaneShape(Base):
    type_ = BPS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            Attr('Normal', pm.Vec3, initDefault=pm.Vec3(0, 0, 1)),
            Attr('Constant', int, initDefault=0),
            parent='BulletBoxShape'
        )


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


import panda3d.core as pm
from panda3d.bullet import BulletWorld as BW
from panda3d.bullet import BulletDebugNode as BDN
from panda3d.bullet import BulletRigidBodyNode as BRBN
from panda3d.bullet import BulletCharacterControllerNode as BCCN

from game.nodes.manager import import_wrapper

Base = import_wrapper('nodes.base.Base')
Attr = import_wrapper('nodes.attributes.Attribute')
Cnnctn = import_wrapper('nodes.attributes.Connection')
CnnctnList = import_wrapper('nodes.attributes.ConnectionList')


class BulletWorld(Base):
    type_ = BW

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AddAttributes(
            Attr('Gravity', pm.Vec3, BW.getGravity, BW.setGravity),
            CnnctnList('Rigid Body', BRBN, BW.getRigidBodies, BW.attachRigidBody, self.ClearRigidBodies,
                       BW.removeRigidBody, self.data),
            CnnctnList('Character', BCCN, BW.getCharacters, BW.attachCharacter, self.ClearCharacters,
                       BW.removeCharacter, self.data),
            Cnnctn('Debug Node', BDN, self.GetDebugNode, BW.setDebugNode, BW.clearDebugNode, self.data),
            parent='BulletWorld'
        )

    def Destroy(self):
        if (base.scene.physicsWorld is self.data and
                base.scene.physicsTask in taskMgr.getAllTasks()):
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

        base.scene.physicsTask = taskMgr.add(update, 'update')

    def DisablePhysics(self):
        taskMgr.remove(base.scene.physicsTask)