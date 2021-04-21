import copy

import panda3d.core as pc
from direct.showbase.PythonUtil import getBase as get_base
from panda3d.core import NodePath as NP
from direct.directtools.DirectSelection import DirectBoundingBox

from pandaEditor import commands
from game.nodes.attributes import Attribute
from game.nodes.constants import TAG_MODEL_ROOT_CHILD
from pandaEditor.nodes.constants import (
    TAG_BBOX, TAG_IGNORE, TAG_MODIFIED, TAG_PICKABLE
)


class NodePath:
    
    geo = None
    pickable = True
    serialise_descendants = True
    
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
    def create(cls, *args, **kwargs):
        comp = super().create(*args, **kwargs)

        # Mark all nodes below this one so as to not serialise them.
        if not cls.serialise_descendants:
            for child in comp.data.find_all_matches('**/*'):
                child.set_python_tag(TAG_MODEL_ROOT_CHILD, True)

        return comp

    @property
    def children(self):
        """
        Return a list of wrappers for the children of this NodePath, ignoring
        those NodePaths tagged with TAG_IGNORE (like editor only geometry).
        """
        return [
            comp
            for comp in super().children
            if not comp.data.get_python_tag(TAG_IGNORE)
        ]

    @property
    def modified(self):
        return self.data.get_python_tag(TAG_MODIFIED)

    @modified.setter
    def modified(self, value):
        if self.data.get_python_tag(TAG_MODEL_ROOT_CHILD):
            self.data.set_python_tag(TAG_MODIFIED, value)

    @property
    def savable(self):
        if self.data.get_python_tag(TAG_MODEL_ROOT_CHILD):
            return self.modified
        else:
            return True
        
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
        
    def set_up_node_path(self):
        super().set_up_node_path()
        
        if self.geo is not None:
            self.geo.copy_to(self.data)
            
        if self.pickable:
            self.data.set_python_tag(TAG_PICKABLE, self.pickable)
            
    def on_select(self):
        """Add a bounding box to the indicated node."""
        bbox = DirectBoundingBox(self.data, (1, 1, 1, 1))
        bbox.show()
        bbox.lines.set_python_tag(TAG_IGNORE, True)
        bbox.lines.node().adjust_draw_mask(*get_base().GetEditorRenderMasks())
        self.data.set_python_tag(TAG_BBOX, bbox)
        return bbox
    
    def on_deselect(self):
        """Remove the bounding box from the indicated node."""
        bbox = self.data.get_python_tag(TAG_BBOX)
        if bbox is not None:
            bbox.lines.remove_node()
        self.data.clear_python_tag(TAG_BBOX)
    
    def on_delete(self, np):
        pass
    
    def get_path(self):
        model_root = self.data.find_net_python_tag(TAG_PICKABLE)
        
        def Rec(tgtNp, np, path):
            if np.compare_to(tgtNp) != 0:
                path.insert(0, np.get_name())
                Rec(tgtNp, np.get_parent(), path)
        
        path = []
        Rec(model_root, self.data, path)
        return '|'.join(path)
    
    def get_attrib(self):
        """
        If this node is a child of a model root, make sure to add its position
        in the hierarchy to the attrib dictionary.
        """
        attrib = super().get_attrib()
        
        if self.modified:
            attrib['path'] = self.get_path()
            
        return attrib
    
    def validate_drag_drop(self, dragComps, dropComp):
        dragNps = [dragComp for dragComp in dragComps if type(dragComp) == pc.NodePath]
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
    
    def on_drag_drop(self, dragComps, dropNp):
        dragNps = [dragComp for dragComp in dragComps if type(dragComp) == pc.NodePath]
        if dragNps:
            commands.Parent(dragNps, dropNp)
            
    def is_of_type(self, cType):
        return self.data.node().is_of_type(cType)
            
    def set_default_values(self):
        pass
        
    @classmethod
    def find_child(cls, *args, **kwargs):

        # TODO: This is pretty dirty. We need to tag a sub-model child
        # on load or else we might lose an edit.
        np = super(NodePath, cls).find_child(*args, **kwargs)
        np.set_python_tag(TAG_MODIFIED, True)
        return np

    @property
    def default_parent(self):
        return get_base().node_manager.wrap(get_base().render)
    
    def on_duplicate(self, orig, dupe):
        super().on_duplicate(orig, dupe)
        
        #wrpr = get_base().node_manager.wrap(orig)
        cnnctns = get_base().scene.get_outgoing_connections(orig)
        print('cnnctns:', cnnctns)
        for cnnctn in cnnctns:
            newCnnctn = copy.copy(cnnctn)
            newCnnctn.connect(self)
        
        self.data.set_python_tag(TAG_MODIFIED, orig.get_python_tag(TAG_MODIFIED))
