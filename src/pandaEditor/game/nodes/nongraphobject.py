from game.nodes.base import Base
from direct.showbase.PythonUtil import getBase as get_base


class Metaobject:

    def __init__(self):
        self.id = None
        self.tags = {}


class NonGraphObject(Base):

    @classmethod
    def create(cls, *args, **kwargs):
        comp = super().create(cls, *args, **kwargs)
        comp._metaobject = Metaobject()
        return comp

    @property
    def metaobject(self):
        return self._metaobject if hasattr(self, '_metaobject') else get_base().scene.objects[self.data]

    def detach(self):
        del get_base().scene.objects[self.data]

    def destroy(self):
        pass

    def add_child(self, child):
        raise NotImplementedError('Cannot parent non graph objects')
