import uuid

import panda3d.core as pc
from panda3d.core import NodePath as NP

from game.nodes.attributes import (
    Connection,
    ConnectionList,
    NodePathAttribute,
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


class NodePath(Base, metaclass=ComponentMetaClass):
    
    type_ = NP
    name = NodePathAttribute(str, pc.NodePath.get_name, pc.NodePath.set_name, init_arg='')
    matrix = NodePathAttribute(pc.Mat4, pc.NodePath.get_mat, pc.NodePath.set_mat)
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
    def Create(cls, *args, **kwargs):
        """
        Create a NodePath with the indicated type and name, set it up and
        return it.
        """
        path = kwargs.pop('path', None)
        if path is None:
            wrpr = super(NodePath, cls).Create(*args, **kwargs)
            wrpr.SetData(pc.NodePath(wrpr.data))
            wrpr.SetupNodePath()
        else:
            wrpr = cls(cls.FindChild(path, kwargs.pop('parent')))
            
        return wrpr
    
    def Detach(self):
        self.data.detachNode()
    
    def Destroy(self):
        
        # Iterate through all addons and destroy them.
        for addon in self.GetAddons():
            addon.Destroy()
            
        self.data.removeNode()
        
    def Duplicate(self, uniqueName=True):
        dupeNp = self.data.copyTo(self.data.getParent())
        
        # Make sure the duplicated NodePath has a unique name to all its 
        # siblings.
        if uniqueName:
            siblingNames = [
                np.getName() 
                for np in self.data.getParent().getChildren()
            ]
            dupeNp.setName(get_unique_name(self.data.getName(), siblingNames))
        
        self.FixUpDuplicateChildren(self.data, dupeNp)
        return dupeNp
    
    def GetId(self):
        return self.data.getTag(TAG_NODE_UUID)
        
    def SetId(self, id):
        self.data.setTag(TAG_NODE_UUID, id)
    
    def GetParent(self):
        if not self.data.getParent().isEmpty():
            return base.node_manager.Wrap(self.data.getParent())
        else:
            return None
    
    def GetChildren(self):
        """Return a list of wrappers for the children of this NodePath."""
        children = [
            base.node_manager.Wrap(cNp)
            for cNp in self.data.getChildren()
        ]
        return children
    
    def GetTags(self):
        tags = self.data.getPythonTag(TAG_PYTHON_TAGS)
        if tags is not None:
            return [tag for tag in tags if tag in base.node_manager.nodeWrappers]
        
        return []
    
    def GetAddons(self):
        addons = []
        
        # Add wrappers for python objects.
        for tag in self.GetTags():
            pyObj = self.data.getPythonTag(tag)
            pyObjWrpr = base.node_manager.Wrap(pyObj)
            addons.append(pyObjWrpr)
            
        return addons
    
    def OnDuplicate(self, origNp, dupeNp):
        
        # If the original NodePath had an id then generate a new one for the 
        # duplicate.
        wrpr = base.node_manager.Wrap(origNp)
        if wrpr.GetId():
            self.CreateNewId()
            
        # Duplicate all addons / objects attached to this NodePath with python
        # tags and set them to the new NodePath.
        for tag in self.GetTags():
            pyObj = origNp.getPythonTag(tag)
            pyObjWrpr = base.node_manager.Wrap(pyObj)
            dupePyObj = pyObjWrpr.Duplicate()
            self.data.setPythonTag(tag, dupePyObj)
        
        return origNp
        
    def SetupNodePath(self):
        self.CreateNewId()
        
    def CreateNewId(self):
        id = str(uuid.uuid4())
        self.data.setTag(TAG_NODE_UUID, id)
        
    def AddChild(self, np):
        np.reparentTo(self.data)
        
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
        
    def GetLights(self, data):
        lgts = []
        
        lgtAttrib = data.getAttrib(pc.LightAttrib)
        if lgtAttrib is not None:
            lgts = lgtAttrib.getOnLights()
        
        return lgts
    
    def GetActor(self):
        """
        Return the actor part of this NodePath if there is one, return None
        otherwise.
        """
        return self.data.getPythonTag(TAG_ACTOR)