from direct.showbase.PythonUtil import getBase as get_base
import panda3d.core as pm

from p3d.object import Object
from p3d.marquee import Marquee
from p3d.mouse import MOUSE_CTRL
from p3d.mousePicker import MousePicker
from nodes.constants import TAG_IGNORE, TAG_PICKABLE


class Selection(Object):

    BBOX_TAG = 'bbox'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.comps = []

        # Create a marquee.
        self.marquee = Marquee('marquee', *args, **kwargs)

        # Create node picker - set its collision mask to hit both geom nodes
        # and collision nodes.
        bitMask = pm.GeomNode.getDefaultCollideMask() | pm.CollisionNode.getDefaultCollideMask()
        self.picker = MousePicker(
            'picker',
            *args,
            fromCollideMask=bitMask, **kwargs
        )

    def get(self):
        """Return the selected components."""
        return self.comps

    @property
    def node_paths(self):
        return [
            comp.data
            for comp in self.comps
            if isinstance(comp.data, pm.NodePath)
        ]

    def clear(self):
        """Clear the selection list and run deselect handlers."""
        for comp in self.comps:
            comp.on_deselect()
        self.comps = []

    def add(self, comps):
        """
        Add the indicated components to the selection and run select handlers.
        """
        for comp in comps:

            # Skip components already selected.
            if comp in self.comps:
                continue
            comp.on_select()
            self.comps.append(comp)

    def remove(self, comps):
        """
        Remove those components that were in the selection and run deselect
        handlers.
        """
        for comp in self.comps:
            comp.on_deselect()
        self.comps = [comp for comp in self.comps if comp not in comps]

    def select_parent(self):
        """
        Return a list of parent components from the selection. Include the
        original component if no suitable parent is found.
        """
        comps = []
        for comp in self.comps:
            pcomp = comp.parent
            if pcomp.data != get_base().scene:
                comps.append(pcomp)
            else:
                comps.append(comp)
        return comps

    def select_child(self):
        """
        Return a list of child components from the selection. Include the
        original component if no children are found.
        """
        comps = []
        for comp in self.comps:
            if comp.children:
                comps.append(comp.children[0])
            else:
                comps.append(comp)
        return comps

    def select_prev(self):
        """
        For each component in the selection, return the component that appears
        one before in the parent's list of children.
        """
        comps = []
        for comp in self.comps:
            children = comp.parent.children

            # Get the index of the child before this one - wrap around if the
            # index has gone below zero.
            index = children.index(comp) - 1
            if index < 0:
                index = len(children) - 1

            comps.append(children[index])
        return comps

    def select_next(self):
        """
        For each component in the selection, return the component that appears
        one after in the parent's list of children.
        """
        comps = []
        for comp in self.comps:
            children = comp.parent.children

            # Get the index of the child after this one - wrap around if the
            # index has gone over the number of children.
            index = children.index(comp) + 1
            if index > len(children) - 1:
                index = 0

            comps.append(children[index])
        return comps

    def StartDragSelect(self, append=False):
        """
        Start the marquee and put the tool into append mode if specified.
        """
        if self.marquee.mouseWatcherNode.hasMouse():
            self.append = append
            self.marquee.Start()

    def StopDragSelect(self):
        """
        Stop the marquee and get all the node paths under it with the correct
        tag. Also append any node which was under the mouse at the end of the
        operation.

        """
        self.marquee.Stop()

        # Find all node paths below the root node which are inside the marquee
        # AND have the TAG_PICKABLE tag.
        nps = []
        for np in self.rootNp.findAllMatches('**'):
            pick_np = self.get_pickable_node_path(np)
            if (
                pick_np is not None and
                self.marquee.IsNodePathInside(pick_np) and
                pick_np not in nps
            ):
                nps.append(pick_np)

        # Add any node path which was under the mouse to the selection.
        np = self.GetNodePathUnderMouse()
        if np is not None and pick_np not in nps:
            nps.append(np)

        # In append mode add any NodePath which wasn't already in the selection
        # and remove any NodePath which was already selected.
        # TODO: This doesn't run deselect handlers.
        comps = [get_base().node_manager.wrap(np) for np in nps]
        if self.append:
            old_comps = self.comps
            for comp in comps:
                if comp in self.comps:
                    old_comps.remove(comp)
                else:
                    old_comps.append(comp)
            comps = old_comps
        return comps

    def GetNodePathUnderMouse(self):
        """
        Returns the closest node under the mouse, or None if there isn't one.

        """
        self.picker.OnUpdate(None)
        pickedNp = self.picker.GetFirstNodePath()
        if pickedNp is not None:
            return self.get_pickable_node_path(pickedNp)
        else:
            return None

    def get_node_path_at_position(self, x, y):
        self.picker.OnUpdate(None, x, y)
        pickedNp = self.picker.GetFirstNodePath()
        if pickedNp is not None:
            return self.get_pickable_node_path(pickedNp)
        else:
            return None

    def get_pickable_node_path(self, np):
        if MOUSE_CTRL in get_base().edCamera.modifiers:
            return np
        return np.findNetPythonTag(TAG_PICKABLE)

    def update(self):
        """Update the selection by running deselect and select handlers."""
        for comp in self.comps:
            comp.on_deselect()
            comp.on_select()
