import logging

from panda3d.core import ConfigVariableBool, loadPrcFileData


editor_mode = ConfigVariableBool('editor_mode', False)
editor_mode.set_value(True)






logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)


from showbase import ShowBase

loadPrcFileData('startup', 'window-type none')

from showbase import ShowBase
ShowBase().run()

import sys
sys.exit()


class EditorBase():

    def hello(self):
        print('hello from EditorBase')


class EditorNodePath(EditorBase):

    def hello(self):
        super().hello()
        print('hello from EditorNodePath')


class EditorLensNode(EditorNodePath):

    def hello(self):
        super().hello()
        print('hello from EditorLensNode')


class EditorCamera(EditorLensNode):

    def hello(self):
        super().hello()
        print('hello from EditorCamera')


editor_classes = {
    'Base': EditorBase,
    'NodePath': EditorNodePath,
    'LensNode': EditorLensNode,
    'Camera': EditorCamera,
}



class WrapperMeta(type):

    def mro(cls):

        mro = super(WrapperMeta, cls).mro()

        print('')
        print(cls)
        print('default:', mro)

        cls_name = cls.__name__
        editor_cls = editor_classes.get(cls_name)
        if editor_cls is not None:
            mro = [editor_cls] + mro

        print('final:', mro)

        return mro


class Base(metaclass=WrapperMeta):

    pass


class NodePath(Base, metaclass=WrapperMeta):

    pass


class LensNode(NodePath, metaclass=WrapperMeta):

    pass


class Camera(LensNode, metaclass=WrapperMeta):

    pass


# np = Camera()
# print('new mro:', np.__class__, np.__class__.mro())
# print(np.__class__.__bases__ )
# import inspect
# print(inspect.getmro(np.__class__))
#np.hello()
#np.hack_mro()
#np.hello()