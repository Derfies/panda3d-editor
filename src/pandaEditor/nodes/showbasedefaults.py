from pandaEditor.nodes.constants import TAG_IGNORE


class Aspect2d:

    @classmethod
    def create(cls, *args, **kwargs):
        comp = super().create(*args, **kwargs)

        # Tag all NodePaths under this node with the ignore tag. They are used
        # to help calculate the aspect ratio and don't need to be saved out or
        # edited. As long as this NodePath wrapper is created before parenting
        # any other NodePaths the user may have created we shouldn't get into
        # much trouble.
        for np in comp.data.get_children():
            np.set_python_tag(TAG_IGNORE, True)
        return comp
