import logging
import unittest

import panda3d.core as pc

from actions import Add, Transform, SetAttribute, Parent
from game.nodes.lights import AmbientLight
from game.nodes.nodepath import NodePath
from game.nodes.showbasedefaults import Render
from pandaEditor.nodes.tests.testmixin import TestMixin


logger = logging.getLogger(__name__)


class TestActions(TestMixin, unittest.TestCase):

    def test_parent(self):
        parent = pc.NodePath(pc.PandaNode('parent'))
        old_parent = pc.NodePath(pc.PandaNode('old_parent'))
        child = pc.NodePath(pc.PandaNode('child'))
        child.reparent_to(old_parent)
        parent_comp = NodePath(parent)
        old_parent_comp = NodePath(old_parent)
        child_comp = NodePath(child)
        action = Parent(child_comp, parent_comp)

        action.redo()
        self.assertEqual(parent, child.get_parent())

        action.undo()
        self.assertEqual(old_parent, child.get_parent())


    def test_add_remove(self):
        light = pc.NodePath(pc.AmbientLight('ambient_light'))
        render = self.base.render
        light_comp, render_comp = AmbientLight(light), Render(render)
        action = Add(light_comp)
        action.pcomp = render_comp
        action.id = 'id'
        action.connections = [(render_comp, 'lights')]

        action.redo()
        self.assertEqual(render, light.get_parent())
        lights = render.get_attrib(pc.LightAttrib).get_on_lights()
        self.assertEqual(light.node(), lights[0].node())

        action.undo()
        self.assertTrue(light.get_parent().is_empty())
        lights = render.get_attrib(pc.LightAttrib)
        self.assertIsNone(lights)

    def test_transform(self):
        panda = pc.NodePath(pc.PandaNode('panda_node'))
        panda_comp = NodePath(panda)
        pos = pc.Point3(1, 0, 0)
        old_pos = pc.Point3(0, 0, 0)
        xform = pc.TransformState.make_pos(pos)
        old_xform = pc.TransformState.make_pos(old_pos)
        action = Transform(panda_comp, xform, old_xform)

        action.redo()
        self.assertEqual(pos, panda.get_pos())

        action.undo()
        self.assertEqual(old_pos, panda.get_pos())

    def test_set_attribute(self):
        panda = pc.NodePath(pc.PandaNode('panda_node'))
        panda_comp = NodePath(panda)
        action = SetAttribute(panda_comp, 'name', 'new_name')

        action.redo()
        self.assertEqual('new_name', panda.get_name())

        action.undo()
        self.assertEqual('panda_node', panda.get_name())
