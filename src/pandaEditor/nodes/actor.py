from direct.showbase.PythonUtil import getBase as get_base

from game.nodes.constants import TAG_MODEL_PATH
from pandaEditor.nodes.constants import TAG_PICKABLE


class Actor:
    
    @classmethod
    def create(cls, *args, **kwargs):
        comp = super().create(*args, **kwargs)
        comp.data.set_python_tag(TAG_PICKABLE, True)
        return comp
    
    def duplicate(self):
        dupe = super().duplicate()
        dupe.set_python_tag(TAG_PICKABLE, True)
        return dupe

    # TODO: Make attribute.
    # def get_full_path(self, node):
    #     model_path = node.get_python_tag(TAG_MODEL_PATH)
    #     rel_path = get_base().project.get_rel_model_path(model_path)
    #     return rel_path
