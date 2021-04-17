from direct.showbase.PythonUtil import getBase as get_base

from game.nodes.constants import TAG_MODEL_ROOT_CHILD


class ModelPathAttribute:

    @property
    def value(self):
        return get_base().project.get_rel_model_path(super().value)


class ModelRoot:
    
    @classmethod
    def create(cls, *args, **kwargs):
        comp = super().create(*args, **kwargs)
        
        # Tag each descendant NodePath as a child of a model root. This edits
        # of these NodePaths to be saved out.
        for child in comp.data.find_all_matches('**/*'):
            child.set_python_tag(TAG_MODEL_ROOT_CHILD, True)
        
        return comp
