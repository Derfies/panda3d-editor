import panda3d.core as pc
from direct.showbase import ShowBaseGlobal
from direct.showbase.PythonUtil import getBase as get_base

from pandaEditor.scene import Scene
from pandaEditor.game.showbase import ShowBase


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

    def tearDown(self):
        """Remove all default nodes and recreate them."""
        # Remove all default nodes and set them to None so they are recreated
        # properly.
        for name in ('cam', 'camera', 'cam2d', 'camera2d'):
            np = getattr(self.base, name)
            np.removeNode()
            setattr(self.base, name, None)

        # Set up render and render2d again, forcing their new values into
        # builtins.
        self.base.setupRender()

        # This is kinda lame imho. These default nodes are created by importing
        # the showbase global module, which makes it difficult to recreate these
        # nodes for our purposes.
        render2d = pc.NodePath('render2d')
        aspect2d = render2d.attachNewNode(pc.PGTop('aspect2d'))
        ShowBaseGlobal.render2d = render2d
        ShowBaseGlobal.aspect2d = aspect2d
        self.base.setupRender2d()

        __builtins__['render'] = self.base.render
        __builtins__['render2d'] = self.base.render2d
        __builtins__['aspect2d'] = self.base.aspect2d
        __builtins__['pixel2d'] = self.base.pixel2d

        self.base.makeCamera(self.base.win)
        self.base.makeCamera2d(self.base.win)
        __builtins__['camera'] = self.base.camera

        # Set auto shader.
        self.base.render.setShaderAuto()

    def test_create(self):
        comp = self.component.create(**self.create_kwargs)
        comp.set_default_parent()
        comp.set_default_values()
        return comp
