import panda3d.core as pc
from direct.showbase.PythonUtil import getBase as get_base

from game.nodes.attributes import (
    Attribute,
    Connection,
    Connections,
)
from game.nodes.constants import (
    TAG_ACTOR,
    TAG_NODE_UUID,
    TAG_PYTHON_TAGS
)
from game.nodes.base import Base
from game.nodes.componentmetaclass import ComponentMetaClass


def get_lights(data):
    attrib = data.get_attrib(pc.LightAttrib)
    return attrib.get_on_lights() if attrib is not None else []


class NodePath(Base, metaclass=ComponentMetaClass):
    
    type_ = pc.NodePath
    name = Attribute(str, pc.NodePath.get_name, pc.NodePath.set_name, required=True)
    color_scale = Attribute(
        pc.LColor,
        pc.NodePath.get_color_scale,
        pc.NodePath.set_color_scale
    )
    matrix = Attribute(pc.Mat4, pc.NodePath.get_mat, pc.NodePath.set_mat)
    texture = Connection(
        pc.Texture,
        pc.NodePath.get_texture,
        pc.NodePath.set_texture,
        pc.NodePath.clear_texture,
    )
    lights = Connections(
        pc.Light,
        get_lights,
        pc.NodePath.set_light,
        pc.NodePath.clear_light,
    )
    fog = Connection(
        pc.Fog,
        pc.NodePath.get_fog,
        pc.NodePath.set_fog,
        pc.NodePath.clear_fog,
        node_target=True,
    )
    
    @classmethod
    def create(cls, *args, **kwargs):
        """
        Create a NodePath with the indicated type and name, set it up and
        return it.

        """
        # For sub-model root nodepaths.
        path = kwargs.pop('path', None)
        if path is not None:
            return cls(cls.find_child(path, kwargs.pop('parent')))

        # Sometimes the data being wrapped is already a node path so this
        # step is unnecessary.
        comp = super().create(*args, **kwargs)
        if not isinstance(comp.data, pc.NodePath):
            comp.data = pc.NodePath(comp.data)
        return comp

    def __hash__(self):

        # An attempt to return an identifier for this node. Note that this is
        # apparently not unique amongst nodepaths that point to the same object,
        # so if this editor ever supports instancing this might fall over
        # spectacularly.
        return hash(self.data.get_key())

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

    @property
    def children(self):
        return [
            get_base().node_manager.wrap(child)
            for child in self.data.get_children()
        ]

    def get_tag(self, name):
        return self.data.get_tag(name)

    def set_tag(self, name, value):
        self.data.set_tag(name, value)
    
    def detach(self):
        self.data.detach_node()
    
    def destroy(self):
        self.data.remove_node()

    @property
    def tags(self):
        tags = self.data.get_python_tag(TAG_PYTHON_TAGS)
        if tags is not None:
            return [
                tag
                for tag in tags
                if tag in get_base().node_manager.wrappers
            ]
        return []
        
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
