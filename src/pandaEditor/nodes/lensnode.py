from game.nodes.attributes import Attribute
from pandaEditor.nodes.constants import TAG_IGNORE


TAG_FRUSTUM = 'P3D_Fustum'


class FrustrumAttribute(Attribute):

    @property
    def value(self):
        """
        Return True if the lens node's frustum is visible, False otherwise.

        """
        return any(
            child.get_python_tag(TAG_FRUSTUM)
            for child in self.parent.data.get_children()
        )

    @value.setter
    def value(self, value):
        """
        Set the camera's frustum to be visible. Ensure it is tagged for removal
        and also so it doesn't appear in any of the scene graph panels.

        """
        if not value:
            self.parent.data.node().hide_frustum()
        else:
            before = set(self.parent.data.get_children())
            self.parent.data.node().show_frustum()
            after = set(self.parent.data.get_children())
            frustum = next(iter(after - before))
            frustum.set_python_tag(TAG_FRUSTUM, True)
            frustum.set_python_tag(TAG_IGNORE, True)


class LensNode:

    show_frustrum = FrustrumAttribute(bool, serialise=False)

    def on_select(self):
        """
        Selection handler. Make sure to disable the frustum if it was shown
        before running the select handler as the frustum will change the size
        of the bounding box.

        """
        visible = self.show_frustrum.value
        self.show_frustrum.value = False
        super().on_select()
        if visible:
            self.show_frustrum.value = True
