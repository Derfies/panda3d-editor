import copy

from direct.showbase.PythonUtil import getBase as get_base

from game.utils import get_lower_camel_case


class NonGraphObject:

    @property
    def label(self):
        return get_lower_camel_case(self.data.__class__.__name__)

    @property
    def default_parent(self):
        return get_base().node_manager.wrap(get_base().scene)

    def duplicate(self):
        dupe = get_base().node_manager.wrap(copy.copy(self.data))
        dupe._metaobject = copy.copy(self.metaobject)
        self.fix_up_duplicate_hierarchy(self, dupe)
        get_base().scene.register_component(dupe)
        return dupe
