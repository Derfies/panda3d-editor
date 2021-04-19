from direct.showbase.PythonUtil import getBase as get_base
import panda3d.core as pm

from p3d.object import Object
from p3d.marquee import Marquee
from p3d.mouse import MOUSE_CTRL
from p3d.mousePicker import MousePicker
from nodes.constants import TAG_IGNORE, TAG_PICKABLE


class Selection(Object):

    BBOX_TAG = 'bbox'

    def __init__(self, base, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.base = base
        self.comps = []
        self.wrprs = []

        # Create a marquee
        self.marquee = Marquee('marquee', *args, **kwargs)

        # Create node picker - set its collision mask to hit both geom nodes
        # and collision nodes
        bitMask = pm.GeomNode.getDefaultCollideMask() | pm.CollisionNode.getDefaultCollideMask()
        self.picker = MousePicker(
            'picker',
            *args,
            fromCollideMask=bitMask, **kwargs
        )

    def Get(self):
        """Return the selected components."""
        return self.comps

    def GetNodePaths(self):
        nps = [
            wrpr.data
            for wrpr in self.wrprs
            if isinstance(wrpr.data, pm.NodePath)
        ]
        return nps

    def Clear(self):
        """Clear the selection list and run deselect handlers."""
        for wrpr in self.wrprs:
            wrpr.on_deselect()
        self.comps = []
        self.wrprs = []

    def Add(self, comps):
        """
        Add the indicated components to the selection and run select handlers.
        """
        for comp in comps:

            # Skip components already selected.
            if comp in self.comps:
                continue

            wrpr = get_base().node_manager.wrap(comp)
            wrpr.on_select()
            self.comps.append(comp)
            self.wrprs.append(wrpr)

    def Remove(self, comps):
        """
        Remove those components that were in the selection and run deselect
        handlers.
        """
        for wrpr in self.wrprs:
            wrpr.on_deselect()

        self.comps = [comp for comp in self.comps if comp not in comps]
        self.wrprs = [get_base().node_manager.wrap(comp) for comp in self.comps]

    def SelectParent(self):
        """
        Return a list of parent components from the selection. Include the
        original component if no suitable parent is found.
        """
        comps = []
        for wrpr in self.wrprs:
            pWrpr = wrpr.parent
            if pWrpr.data != get_base().scene:
                comps.append(pWrpr.data)
            else:
                comps.append(wrpr.data)
        return comps

    def SelectChild(self):
        """
        Return a list of child components from the selection. Include the
        original component if no children are found.
        """
        comps = []
        for wrpr in self.wrprs:
            if wrpr.children:
                comps.append(wrpr.children[0].data)
            else:
                comps.append(wrpr.data)
        return comps

    def SelectPrev(self):
        """
        For each component in the selection, return the component that appears
        one before in the parent's list of children.
        """
        comps = []
        for wrpr in self.wrprs:
            pWrpr = wrpr.parent
            cComps = [cWrpr.data for cWrpr in pWrpr.children]

            # Get the index of the child before this one - wrap around if the
            # index has gone below zero.
            index = cComps.index(wrpr.data) - 1
            if index < 0:
                index = len(cComps) - 1

            comps.append(cComps[index])
        return comps

    def SelectNext(self):
        """
        For each component in the selection, return the component that appears
        one after in the parent's list of children.
        """
        comps = []
        for wrpr in self.wrprs:
            pWrpr = wrpr.parent
            cComps = [cWrpr.data for cWrpr in pWrpr.children]

            # Get the index of the child after this one - wrap around if the
            # index has gone over the number of children.
            index = cComps.index(wrpr.data) + 1
            if index > len(cComps) - 1:
                index = 0

            comps.append(cComps[index])
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
            pick_np = self.GetPickableNodePath(np)
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
        if self.append:
            oldComps = self.comps
            for np in nps:
                if np in self.comps:
                    oldComps.remove(np)
                else:
                    oldComps.append(np)
            nps = oldComps

        return nps

    def GetNodePathUnderMouse(self):
        """
        Returns the closest node under the mouse, or None if there isn't one.
        """
        self.picker.OnUpdate(None)
        pickedNp = self.picker.GetFirstNodePath()
        if pickedNp is not None:
            return self.GetPickableNodePath(pickedNp)
        else:
            return None

    def GetNodePathAtPosition(self, x, y):
        self.picker.OnUpdate(None, x, y)
        pickedNp = self.picker.GetFirstNodePath()
        if pickedNp is not None:
            return self.GetPickableNodePath(pickedNp)
        else:
            return None

    def GetPickableNodePath(self, np):
        # if MOUSE_CTRL not in get_base().edCamera.mouse.modifiers:
        #     np = np.findNetPythonTag(TAG_PICKABLE)
        # return None if np.isEmpty() else np
        if np.getPythonTag(TAG_IGNORE):
            return np.findNetPythonTag(TAG_PICKABLE)
        elif MOUSE_CTRL in get_base().edCamera.mouse.modifiers:
           return np
        else:
            return np.findNetPythonTag(TAG_PICKABLE)

    def Update(self):
        """Update the selection by running deselect and select handlers."""
        for wrpr in self.wrprs:
            wrpr.on_deselect()
            wrpr.on_select()
