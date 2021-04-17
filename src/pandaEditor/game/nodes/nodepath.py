import uuid

from direct.showbase.PythonUtil import getBase as get_base
import panda3d.core as pc
#from direct.showbase.PythonUtil import getBase as get_base
from panda3d.core import NodePath as NP

from game.nodes.attributes import (
    Attribute,
    Connection,
    ConnectionList,
    NodeConnection,
    #NodePathAttribute,
    NodePathTargetConnection
)
from game.nodes.constants import (
    TAG_ACTOR,
    TAG_NODE_UUID,
    TAG_PYTHON_TAGS
)
from game.nodes.base import Base
from game.nodes.othermeta import ComponentMetaClass
from game.utils import get_unique_name


class Lights(ConnectionList):

    def __init__(self):
        super().__init__(
            pc.Light,
            self.get_lights,
            pc.NodePath.set_light,
            pc.NodePath.clear_light,
        )

    def get_lights(self, data):
        attrib = data.get_attrib(pc.LightAttrib)
        return attrib.get_on_lights() if attrib is not None else None


class NodePath(Base, metaclass=ComponentMetaClass):
    
    type_ = NP
    name = Attribute(str, pc.NodePath.get_name, pc.NodePath.set_name, init_arg='')
    matrix = Attribute(pc.Mat4, pc.NodePath.get_mat, pc.NodePath.set_mat)
    lights = Lights()
    fog = NodeConnection(pc.Fog, pc.NodePath.get_fog, pc.NodePath.set_fog, pc.NodePath.clear_fog)
    # matrix = NodePathAttribute('', pc.Mat4, pc.NodePath.get_mat,
    #                            pc.NodePath.set_mat)
    # matrix = NodePathAttribute('', pc.Mat4, pc.NodePath.get_mat,
    #                            pc.NodePath.set_mat)
    # matrix = NodePathAttribute('', pc.Mat4, pc.NodePath.get_mat,
    #                            pc.NodePath.set_mat)

    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     self.AddAttributes(
    #         NodePathAttribute('Name', str, NP.getName, NP.setName, init_arg=''),
    #         NodePathAttribute('Matrix', pc.Mat4, NP.getMat, NP.setMat),
    #         ConnectionList('Lights', pc.Light, self.GetLights, NP.setLight, NP.clearLight, NP.clearLight),
    #         Connection('Texture', pc.Texture, NP.getTexture, NP.setTexture, NP.clearTexture, args=[1]),
    #         NodePathTargetConnection('Fog ', pc.Fog, NP.getFog, NP.setFog, NP.clearFog),
    #         Connection('Shader', pc.Filename, self.GetShader, self.SetShader, NP.clearShader),
    #         parent='NodePath'
    #    )
    
    @classmethod
    def create(cls, *args, **kwargs):
        """
        Create a NodePath with the indicated type and name, set it up and
        return it.
        """
        path = kwargs.pop('path', None)
        if path is None:
            wrpr = super(NodePath, cls).create(*args, **kwargs)
            wrpr.data = pc.NodePath(wrpr.data)
            wrpr.set_up_node_path()
        else:
            wrpr = cls(cls.FindChild(path, kwargs.pop('parent')))
            
        return wrpr

    @property
    def id(self):
        return self.data.get_tag(TAG_NODE_UUID)

    @id.setter
    def id(self, value):
        self.data.set_tag(TAG_NODE_UUID, value)

    @Base.parent.getter
    def parent(self):
        return get_base().node_manager.wrap(self.data.get_parent())
        # if not self.data.parent.data.is_empty():
        #     return get_base().node_manager.wrap(self.data.get_parent())
        # else:
        #     return None

    # @Base.parent.setter
    # def parent(self, value):
    #     super().parent(value)
    
    def detach(self):
        self.data.detach_node()
    
    def destroy(self):
        
        # Iterate through all addons and destroy them.
        for addon in self.get_add_ons():
            addon.destroy()
            
        self.data.remove_node()
        
    def duplicate(self, uniqueName=True):
        dupeNp = self.data.copyTo(self.data.getParent())
        
        # Make sure the duplicated NodePath has a unique name to all its 
        # siblings.
        if uniqueName:
            siblingNames = [
                np.getName() 
                for np in self.data.getParent().getChildren()
            ]
            dupeNp.setName(get_unique_name(self.data.getName(), siblingNames))
        
        self.fix_up_duplicate_children(self.data, dupeNp)
        return dupeNp
    
    def get_children(self):
        return [
            get_base().node_manager.wrap(np)
            for np in self.data.get_children()
        ]
    
    def GetTags(self):
        tags = self.data.getPythonTag(TAG_PYTHON_TAGS)
        if tags is not None:
            return [tag for tag in tags if tag in base.node_manager.nodeWrappers]
        
        return []
    
    def get_add_ons(self):
        addons = []
        
        # Add wrappers for python objects.
        for tag in self.GetTags():
            pyObj = self.data.getPythonTag(tag)
            pyObjWrpr = base.node_manager.wrap(pyObj)
            addons.append(pyObjWrpr)
            
        return addons
    
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
    def FindChild(cls, path, parent):
        buffer = path.split('|')
        np = parent
        for elem in buffer:
            childNames = [child.getName() for child in np.getChildren()]
            index = childNames.index(elem)
            np = np.getChildren()[index]
                    
        return np
    
    def GetShader(self, np):
        shader = np.getShader()
        if shader is None:
            return ''
        
        return shader.getFilename()
        
    def SetShader(self, np, filePath):
        try:
            pandaPath = pc.Filename.fromOsSpecific(filePath)
        except TypeError:
            pandaPath = filePath
        shader = pc.Shader.load(pandaPath)
        if shader is not None:
            np.setShader(shader)
        else:
            np.clearShader()
        
    def get_lights(self, data):
        attrib = data.get_attrib(pc.LightAttrib)
        return attrib.get_on_lights() if attrib is not None else None

    def GetActor(self):
        """
        Return the actor part of this NodePath if there is one, return None
        otherwise.
        """
        return self.data.getPythonTag(TAG_ACTOR)
