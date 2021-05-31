import unittest

import panda3d.bullet as pb
import panda3d.core as pc
from direct.showbase.PythonUtil import getBase as get_base
from game.nodes.bullet import (
    BulletBoxShape,
    BulletCapsuleShape,
    BulletDebugNode,
    BulletPlaneShape,
    BulletRigidBodyNode,
    BulletSphereShape,
    BulletWorld,
)
from game.nodes.nongraphobject import Metaobject
from pandaEditor.nodes.tests.testbasemixin import TestBaseMixin
from pandaEditor.nodes.tests.test_nodepath import TestNodePathMixin


class TestBulletBoxShape(TestBaseMixin, unittest.TestCase):

    component = BulletBoxShape
    create_kwargs = {
        'halfExtents': pc.Vec3(0.5, 0.5, 0.5),
    }


class TestBulletCapsuleShape(TestBaseMixin, unittest.TestCase):

    component = BulletCapsuleShape
    create_kwargs = {
        'radius': 0.5,
        'height': 1,
        'up': pb.ZUp,
    }


class TestBulletDebugNode(TestNodePathMixin, unittest.TestCase):

    component = BulletDebugNode


class TestBulletPlaneShape(TestBaseMixin, unittest.TestCase):

    component = BulletPlaneShape
    create_kwargs = {
        'normal': pc.Vec3(0, 0, 1),
        'point': pc.Vec3(0, 0, 0),
    }


class TestBulletRigidBodyNode(TestBaseMixin, unittest.TestCase):

    component = BulletRigidBodyNode

    def test_append_shape(self):
        rigid, shape = pc.NodePath(pb.BulletRigidBodyNode()), pb.BulletSphereShape(1)
        rigid_comp, shape_comp = BulletRigidBodyNode(rigid), BulletSphereShape(shape)
        self.base.scene.objects[shape_comp.data] = Metaobject()
        rigid_comp.shapes.append(shape_comp)
        self.assertEqual(shape, rigid.node().get_shapes()[0])

    def test_remove_solid(self):
        rigid, shape = pc.NodePath(pb.BulletRigidBodyNode()), pb.BulletSphereShape(1)
        rigid.node().add_shape(shape)
        rigid_comp, shape_comp = BulletRigidBodyNode(rigid), BulletSphereShape(shape)
        rigid_comp.shapes.remove(shape_comp)
        self.assertEqual(0, len(rigid.node().get_shapes()))


class TestBulletSphereShape(TestBaseMixin, unittest.TestCase):

    component = BulletSphereShape
    create_kwargs = {
        'radius': 0.5,
    }


class TestBulletWorld(TestBaseMixin, unittest.TestCase):

    component = BulletWorld

    def test_create(self):
        super().test_create()
        self.assertIsNotNone(get_base().scene.physics_world)

    def test_set_debug_node(self):
        world, debug = pb.BulletWorld(), pc.NodePath(pb.BulletDebugNode())
        world_comp, debug_comp = BulletWorld(world), BulletDebugNode(debug)
        world_comp.debug_node = debug_comp
        self.assertEqual(debug.node(), world.get_debug_node())

    def test_append_rigid_body(self):
        world, rigid = pb.BulletWorld(), pc.NodePath(pb.BulletRigidBodyNode())
        world_comp, rigid_comp = BulletWorld(world), BulletRigidBodyNode(rigid)
        world_comp.rigid_bodies.append(rigid_comp)
        self.assertEqual(rigid.node(), world.get_rigid_bodies()[0])

    def test_remove_rigid_body(self):
        world, rigid = pb.BulletWorld(), pc.NodePath(pb.BulletRigidBodyNode())
        world.attach(rigid.node())
        world_comp, rigid_comp = BulletWorld(world), BulletRigidBodyNode(rigid)
        world_comp.rigid_bodies.remove(rigid_comp)
        self.assertEqual(0, len(world.get_rigid_bodies()))
