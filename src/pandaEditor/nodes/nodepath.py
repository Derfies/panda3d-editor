import collections
import logging

import panda3d.core as pc
from direct.showbase.PythonUtil import getBase as get_base
from direct.directtools.DirectSelection import DirectBoundingBox

from pandaEditor import commands
from game.nodes.attributes import Attribute
from game.nodes.constants import TAG_MODEL_ROOT_CHILD
from game.utils import get_lower_camel_case, get_unique_name
from pandaEditor.nodes.constants import (
    TAG_BBOX, TAG_IGNORE, TAG_MODIFIED, TAG_PICKABLE
)


logger = logging.getLogger(__name__)


class NodePath:
    
    geo = None
    pickable = True
    serialise_descendants = True
    position = Attribute(
        pc.Vec3,
        pc.NodePath.get_pos,
        pc.NodePath.set_pos,
        serialise=False
    )
    rotation = Attribute(
        pc.Vec3,
        pc.NodePath.get_hpr,
        pc.NodePath.set_hpr,
        serialise=False
    )
    scale = Attribute(
        pc.Vec3,
        pc.NodePath.get_scale,
        pc.NodePath.set_scale,
        serialise=False
    )

    @property
    def label(self):
        return self.name

    @classmethod
    def get_default_values(cls):
        default_values = super().get_default_values()
        default_values.update({
            'name': get_lower_camel_case(cls.__name__)
        })
        return default_values

    @classmethod
    def get_foo(cls):
        foo = super().get_foo()
        foo.remove('name')
        return foo

    @classmethod
    def create(cls, *args, **kwargs):
        comp = super().create(*args, **kwargs)

        # Mark all nodes below this one so as to not serialise them.
        if not cls.serialise_descendants:
            for child in comp.data.find_all_matches('**/*'):
                child.set_python_tag(TAG_MODEL_ROOT_CHILD, True)

        # Copy any helper geo to the new instance.
        if comp.geo is not None:
            comp.geo.copy_to(comp.data)

        # Mark as pickable.
        if comp.pickable:
            comp.data.set_python_tag(TAG_PICKABLE, comp.pickable)

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
        for child in geo.find_all_matches('**'):
            child.set_python_tag(TAG_IGNORE, True)
        geo.set_light_off()
        geo.node().adjust_draw_mask(*get_base().GetEditorRenderMasks())
        cls.geo = geo
            
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

    def duplicate(self, make_unique=True):
        dupe_np = self.data.copy_to(self.data.get_parent())

        # Make sure the duplicated NodePath has a unique name to all its
        # siblings.
        if make_unique:
            sibling_names = [
                sib.data.get_name()
                for sib in self.parent.children
            ]
            unique_name = get_unique_name(self.data.get_name(), sibling_names)
            dupe_np.set_name(unique_name)
        dupe = get_base().node_manager.wrap(dupe_np)
        self.fix_up_duplicate_hierarchy(self, dupe)

        return get_base().node_manager.wrap(dupe_np)

    def fix_up_duplicate_hierarchy(self, orig, dupe):

        # Connect the duplicated node in a similar fashion to the original node.
        conns = get_base().scene.get_outgoing_connections(orig)
        for target, conn_name in conns:
            value = getattr(target, conn_name)
            if isinstance(value, collections.MutableSequence):
                value.append(dupe)
            else:
                raise NotImplementedError('cant do that yet')

        super().fix_up_duplicate_hierarchy(orig, dupe)
