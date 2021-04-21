import uuid

import panda3d.core as pc
from direct.showbase.PythonUtil import getBase as get_base

from game.nodes.attributes import (
    Attribute,
    Connections,
    ToNodeConnection,
)
from game.nodes.constants import (
    TAG_ACTOR,
    TAG_NODE_UUID,
    TAG_PYTHON_TAGS
)
from game.nodes.base import Base
from game.nodes.componentmetaclass import ComponentMetaClass
from game.utils import get_unique_name


def get_lights(data):
    attrib = data.get_attrib(pc.LightAttrib)
    return attrib.get_on_lights() if attrib is not None else []


class NodePath(Base, metaclass=ComponentMetaClass):
    
    type_ = pc.NodePath
    name = Attribute(str, pc.NodePath.get_name, pc.NodePath.set_name, init_arg='')
    color_scale = Attribute(
        pc.LColor,
        pc.NodePath.get_color_scale,
        pc.NodePath.set_color_scale
    )
    matrix = Attribute(pc.Mat4, pc.NodePath.get_mat, pc.NodePath.set_mat)
    lights = Connections(
        pc.Light,
        get_lights,
        pc.NodePath.set_light,
        pc.NodePath.clear_light,
        pc.NodePath.clear_light,
    )
    fog = ToNodeConnection(
        pc.Fog,
        pc.NodePath.get_fog,
        pc.NodePath.set_fog,
        pc.NodePath.clear_fog
    )
    
    @classmethod
    def create(cls, *args, **kwargs):
        """
        Create a NodePath with the indicated type and name, set it up and
        return it.

        """
        path = kwargs.pop('path', None)
        if path is not None:
            return cls(cls.find_child(path, kwargs.pop('parent')))

        # Sometimes the data being wrapped is already a node path so this
        # step is unnecessary.
        comp = super().create(*args, **kwargs)
        if not isinstance(comp.data, pc.NodePath):
            comp.data = pc.NodePath(comp.data)
        comp.set_up_node_path()
        return comp

    @property
    def id(self):
        return self.data.get_tag(TAG_NODE_UUID)

    @id.setter
    def id(self, value):
        self.data.set_tag(TAG_NODE_UUID, value)

    @Base.parent.getter
    def parent(self):
        parent_np = self.data.get_parent()
        if not parent_np.is_empty():
            return get_base().node_manager.wrap(parent_np)
        else:
            return None
    
    def detach(self):
        self.data.detach_node()
    
    def destroy(self):
        self.data.remove_node()
        
    def duplicate(self, unique_name=True):
        dupe_np = self.data.copyTo(self.data.get_parent())
        
        # Make sure the duplicated NodePath has a unique name to all its 
        # siblings.
        if unique_name:
            sibling_names = [
                np.get_name()
                for np in self.data.get_parent().get_children()
            ]
            dupe_np.set_name(get_unique_name(self.data.get_name(), sibling_names))
        
        self.fix_up_duplicate_children(self.data, dupe_np)
        return dupe_np

    @property
    def children(self):
        return [
            get_base().node_manager.wrap(child)
            for child in self.data.get_children()
        ]
    
    def GetTags(self):
        tags = self.data.getPythonTag(TAG_PYTHON_TAGS)
        if tags is not None:
            return [tag for tag in tags if tag in base.node_manager.nodeWrappers]
        
        return []

    def on_duplicate(self, origNp, dupeNp):
        
        # If the original NodePath had an id then generate a new one for the 
        # duplicate.
        wrpr = base.node_manager.wrap(origNp)
        if wrpr.id:
            self.create_new_id()
            
        # Duplicate all addons / objects attached to this NodePath with python
        # tags and set them to the new NodePath.
        for tag in self.GetTags():
            pyObj = origNp.getPythonTag(tag)
            pyObjWrpr = base.node_manager.wrap(pyObj)
            dupePyObj = pyObjWrpr.duplicate()
            self.data.setPythonTag(tag, dupePyObj)
        
        return origNp
        
    def set_up_node_path(self):
        self.create_new_id()
        
    def create_new_id(self):
        self.id = str(uuid.uuid4())
        
    def add_child(self, child):
        child.data.reparent_to(self.data)
        
    @classmethod
    def find_child(cls, path, parent):
        buffer = path.split('|')
        np = parent.data
        for elem in buffer:
            child_names = [child.get_name() for child in np.get_children()]
            index = child_names.index(elem)
            np = np.get_children()[index]
                    
        return np

    def GetActor(self):
        """
        Return the actor part of this NodePath if there is one, return None
        otherwise.
        """
        return self.data.getPythonTag(TAG_ACTOR)
