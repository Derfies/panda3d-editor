import unittest

import panda3d.core as pc
from game.nodes.collision import (
    CollisionBox,
    CollisionCapsule,
    CollisionInvSphere,
    CollisionNode,
    CollisionRay,
    CollisionSphere,
)
from game.nodes.nongraphobject import Metaobject
from pandaEditor.nodes.tests.test_nodepath import (
    TestNodePathMixin,
)
from pandaEditor.nodes.tests.testbasemixin import TestBaseMixin


class TestCollisionBox(TestBaseMixin, unittest.TestCase):

    component = CollisionBox
    create_kwargs = {
        'min': pc.Point3(-0.5, -0.5, -0.5),
        'max': pc.Point3(0.5, 0.5, 0.5),
    }


class TestCollisionCapsule(TestBaseMixin, unittest.TestCase):

    component = CollisionCapsule
    create_kwargs = {
        'a': pc.Point3(0),
        'db': pc.Point3(0, 0, 1),
        'radius': 0.5,
    }


class TestCollisionNode(TestNodePathMixin, unittest.TestCase):

    component = CollisionNode

    def test_append_solid(self):
        collision = pc.NodePath(pc.CollisionNode('collision_node'))
        solid = pc.CollisionBox(pc.Point3(0, 0, 0), 1, 1, 1)
        node_comp, solid_comp = CollisionNode(collision), CollisionBox(solid)
        self.base.scene.objects[solid_comp.data] = Metaobject()
        node_comp.solids.append(solid_comp)
        self.assertEqual(solid, collision.node().get_solids()[0])

    def test_remove_solid(self):
        collision = pc.NodePath(pc.CollisionNode('collision_node'))
        solid = pc.CollisionBox(pc.Point3(0, 0, 0), 1, 1, 1)
        collision.node().add_solid(solid)
        node_comp, solid_comp = CollisionNode(collision), CollisionBox(solid)
        node_comp.solids.remove(solid_comp)
        self.assertEqual(0, len(collision.node().get_solids()))


class TestCollisionRay(TestBaseMixin, unittest.TestCase):

    component = CollisionRay
    create_kwargs = {
        'origin': pc.Point3(0),
        'direction': pc.Vec3(0, 0, 1),
    }


class TestCollisionSphere(TestBaseMixin, unittest.TestCase):

    component = CollisionSphere
    create_kwargs = {
        'center': pc.Point3(0),
        'radius': 0.5,
    }


class TestCollisionInvSphere(TestCollisionSphere):

    component = CollisionInvSphere
    create_kwargs = {
        'center': pc.Point3(0),
        'radius': 0.5,
    }
