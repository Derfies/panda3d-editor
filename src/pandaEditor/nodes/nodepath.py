import copy

import panda3d.core as pm
from panda3d.core import NodePath as NP
from direct.directtools.DirectSelection import DirectBoundingBox

from pandaEditor import commands
from game.nodes.attributes import NodePathAttribute
from game.nodes.constants import TAG_MODEL_ROOT_CHILD
from pandaEditor.nodes.constants import (
    TAG_BBOX, TAG_IGNORE, TAG_MODIFIED, TAG_PICKABLE
)


class NodePath:
    
    geo = None
    pickable = True
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     # Find the index of the 'name' property so we can add position,
    #     # rotation and scale properties immediately after it.
    #     i = self.attributes.index(self.FindProperty('name'))
    #
    #     # Add attributes for position, rotation and scale. These are
    #     # implemented editor side only as we only need a matrix to xform the
    #     # NodePath; they are for the user's benefit only.
    #     self.AddAttributes(NodePathAttribute('Position', pm.Vec3, NP.getPos, NP.setPos, w=False), index=i + 1)
    #     self.AddAttributes(
    #         NodePathAttribute('X', float, NP.getX, NP.setX, w=False),
    #         NodePathAttribute('Y', float, NP.getY, NP.setY, w=False),
    #         NodePathAttribute('Z', float, NP.getZ, NP.setZ, w=False),
    #         parent='Position'
    #   )
    #
    #     self.AddAttributes(NodePathAttribute('Rotation', pm.Vec3, NP.getHpr, NP.setHpr, w=False), index=i + 2)
    #     self.AddAttributes(
    #         NodePathAttribute('H', float, NP.getH, NP.setH, w=False),
    #         NodePathAttribute('P', float, NP.getP, NP.setP, w=False),
    #         NodePathAttribute('R', float, NP.getR, NP.setR, w=False),
    #         parent='Rotation'
    #   )
    #
    #     self.AddAttributes(NodePathAttribute('Scale', pm.Vec3, NP.getScale, NP.setScale, w=False), index=i + 3)
    #     self.AddAttributes(
    #         NodePathAttribute('Sx', float, NP.getSx, NP.setSx, w=False),
    #         NodePathAttribute('Sy', float, NP.getSy, NP.setSy, w=False),
    #         NodePathAttribute('Sz', float, NP.getSz, NP.setSz, w=False),
    #         parent='Scale'
    #   )
        
    @classmethod
    def SetPickable(cls, value=True):
        cls.pickable = value
        
    @classmethod
    def set_editor_geometry(cls, geo):
        """
        Set the indicated geometry to be used as a proxy for the NodePath. 
        Tag all descendant NodePaths with the ignore tag so they don't show up
        in the scene graph and cannot be selected.
        """
        for childNp in geo.findAllMatches('**'):
            childNp.setPythonTag(TAG_IGNORE, True)
        geo.setLightOff()
        geo.node().adjustDrawMask(*base.GetEditorRenderMasks())
        cls.geo = geo
        
    def SetupNodePath(self):
        super().SetupNodePath()
        
        if self.geo is not None:
            self.geo.copyTo(self.data)
            
        if self.pickable:
            self.data.setPythonTag(TAG_PICKABLE, self.pickable)
            
    def OnSelect(self):
        """Add a bounding box to the indicated node."""
        bbox = DirectBoundingBox(self.data, (1, 1, 1, 1))
        bbox.show()
        bbox.lines.setPythonTag(TAG_IGNORE, True)
        bbox.lines.node().adjustDrawMask(*base.GetEditorRenderMasks())
        self.data.setPythonTag(TAG_BBOX, bbox)
        return bbox
    
    def OnDeselect(self):
        """Remove the bounding box from the indicated node."""
        bbox = self.data.getPythonTag(TAG_BBOX)
        if bbox is not None:
            bbox.lines.removeNode()
        self.data.clearPythonTag(TAG_BBOX)
    
    def OnDelete(self, np):
        pass
    
    def GetPath(self):
        modelRoot = self.data.findNetPythonTag(TAG_PICKABLE)
        
        def Rec(tgtNp, np, path):
            if np.compareTo(tgtNp) != 0:
                path.insert(0, np.getName())
                Rec(tgtNp, np.getParent(), path)
        
        path = []
        Rec(modelRoot, self.data, path)
        return '|'.join(path)
    
    def GetAttrib(self):
        """
        If this node is a child of a model root, make sure to add its position
        in the hierarchy to the attrib dictionary.
        """
        attrib = super().GetAttrib()
        
        if self.GetModified():
            attrib['path'] = self.GetPath()
            
        return attrib
    
    def GetModified(self):
        return self.data.getPythonTag(TAG_MODIFIED)
    
    def SetModified(self, val):
        if self.data.getPythonTag(TAG_MODEL_ROOT_CHILD):
            self.data.setPythonTag(TAG_MODIFIED, val)
    
    def ValidateDragDrop(self, dragComps, dropComp):
        dragNps = [dragComp for dragComp in dragComps if type(dragComp) == pm.NodePath]
        if not dragNps:
            return False
        
        # If the drop item is none then the drop item will default to the
        # root node. No other checks necessary.
        if dropComp is None:
            return True
            
        # Fail if the drop item is one of the items being dragged
        #dropNp = dropItem.GetData()
        if dropComp in dragComps:
            return False
        
        # Fail if the drag items are ancestors of the drop items
        if True in [comp.isAncestorOf(dropComp) for comp in dragComps]:
            return False
        
        # Drop target item is ok, continue
        return True
    
    def OnDragDrop(self, dragComps, dropNp):
        dragNps = [dragComp for dragComp in dragComps if type(dragComp) == pm.NodePath]
        if dragNps:
            commands.Parent(dragNps, dropNp)
            
    def IsOfType(self, cType):
        return self.data.node().isOfType(cType)
            
    def SetDefaultValues(self):
        pass
        
    def IsSaveable(self):
        if self.data.getPythonTag(TAG_MODEL_ROOT_CHILD):
            return self.GetModified()
        else:
            return True
        
    @classmethod
    def FindChild(cls, *args, **kwargs):
        np = super(NodePath, cls).FindChild(*args, **kwargs)
        np.setPythonTag(TAG_MODIFIED, True)
        return np
    
    def GetDefaultParent(self):
        return base.render
    
    def GetChildren(self):
        """
        Return a list of wrappers for the children of this NodePath, ignoring
        those NodePaths tagged with TAG_IGNORE (like editor only geometry).
        """
        children = [
            cWrpr 
            for cWrpr in super().GetChildren()
            if not cWrpr.data.getPythonTag(TAG_IGNORE)
        ]
        return children
    
    def OnDuplicate(self, origNp, dupeNp):
        super().OnDuplicate(origNp, dupeNp)
        
        wrpr = base.node_manager.Wrap(origNp)
        cnnctns = base.scene.GetOutgoingConnections(wrpr)
        for cnnctn in cnnctns:
            newCnnctn = copy.copy(cnnctn)
            newCnnctn.Connect(self.data)
        
        self.data.setPythonTag(TAG_MODIFIED, origNp.getPythonTag(TAG_MODIFIED))