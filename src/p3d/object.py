from direct.showbase.PythonUtil import getBase as get_base
from direct.showbase.DirectObject import DirectObject


class Object(DirectObject):

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.camera = kwargs.pop('camera', get_base().camera)
        self.rootNp = kwargs.pop('rootNp', get_base().render)
        self.root2d = kwargs.pop('root2d', get_base().render2d)
        self.rootA2d = kwargs.pop('rootA2d', get_base().aspect2d)
        self.rootP2d = kwargs.pop('rootP2d', get_base().pixel2d)
        self.win = kwargs.pop('win', get_base().win)
        self.mouseWatcherNode = kwargs.pop(
            'mouseWatcherNode',
            get_base().mouseWatcherNode
        )
