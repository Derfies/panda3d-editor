import abc

from direct.showbase.PythonUtil import getBase as get_base
from panda3d.core import ConfigVariableString, ConfigVariableBool


ConfigVariableBool('editor_mode', False).set_value(True)
ConfigVariableBool('no_ui', False).set_value(True)
# ConfigVariableString('window-type', 'none').setValue('none')
# from pandaEditor.game.showbase import ShowBase as GameShowBase
# from pandaEditor.showbase import GameShowBase
from direct.showbase.ShowBase import ShowBase# as DirectShowBase


class TestShowBase(ShowBase):

    pass


class TestBaseMixin:

    component = None
    create_kwargs = {}

    def setUp(self):
        try:
            self.base = get_base()
        except:
            self.base = TestShowBase()

    def test_create(self):
        node = self.component.create(**self.create_kwargs)
        return node


class ComponentMixin(TestBaseMixin):

    def test_create(self):
        node = super().test_create()
        self.assertIsNone(node.lights.get())
        self.assertIsNone(node.fog.get())
        return node
