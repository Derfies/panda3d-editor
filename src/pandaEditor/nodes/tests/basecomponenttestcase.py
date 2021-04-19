import abc
import uuid

from direct.showbase.PythonUtil import getBase as get_base
from panda3d.core import ConfigVariableString, ConfigVariableBool


ConfigVariableBool('editor_mode', False).set_value(True)
ConfigVariableBool('no_ui', False).set_value(True)


from pandaEditor.scene import Scene
from pandaEditor.game.showbase import ShowBase
# class TestScene:
#
#     # TODO: Need to figure out a better way to do this.
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         self.comps = {}
#
#     def register_component(self, comp):
#         self.comps[comp] = str(uuid.uuid4())


class TestShowBase(ShowBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scene = Scene()


class TestBaseMixin:

    component = None
    create_kwargs = {}

    def setUp(self):
        try:
            self.base = get_base()
        except NameError:
            self.base = TestShowBase()

    def test_create(self):
        node = self.component.create(**self.create_kwargs)
        return node
