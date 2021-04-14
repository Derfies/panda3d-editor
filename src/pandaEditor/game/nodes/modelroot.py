import panda3d.core as pm
from panda3d.core import ModelRoot as MR

from game.nodes.attributes import NodeAttribute
from game.nodes.constants import (
    TAG_MODEL_ROOT_CHILD, TAG_NODE_TYPE
)
from game.nodes.nodepath import NodePath


class ModelRoot(NodePath):
    
    type_ = pm.ModelRoot
    
    def __init__(self, *args, **kwargs):
        NodePath.__init__(self, *args, **kwargs)
        
        self.AddAttributes(
            NodeAttribute('ModelPath', pm.Filename, self.GetFullPath, initDefault=''),
            parent='ModelRoot'
       )
    
    @classmethod
    def Create(cls, *args, **kwargs):
        modelPath = kwargs.pop('modelPath', '')
        if not modelPath:
            np = pm.NodePath(pm.ModelRoot(''))
        else:
            filePath = pm.Filename.fromOsSpecific(modelPath)
            try:
                np = loader.loadModel(filePath)
            except:
                try:
                    np = loader.loadModel(filePath + '.bam')
                except IOError:
                    print('Failed to load: ', filePath)
                    np = pm.NodePath(pm.ModelRoot(''))
            np.setName(filePath.getBasenameWoExtension())
        
        wrpr = cls(np)
        wrpr.SetupNodePath()
        
        # Iterate over child nodes
        wrpr.extraNps = []
        def Recurse(node):
            nTypeStr = node.getTag(TAG_NODE_TYPE)
            cWrprCls = base.node_manager.GetWrapperByName(nTypeStr)
            if cWrprCls is not None:
                cWrpr = cWrprCls.Create(inputNp=node)
                wrpr.extraNps.append(cWrpr.data)
            
            # Recurse
            for child in node.getChildren():
                Recurse(child)
                
        Recurse(np)
        
        return wrpr
    
    def AddChild(self, np):
        """
        Parent the indicated NodePath to the NodePath wrapped by this object.
        We don't have to parent NodePaths with the model root tag as they were
        created with the correct hierarchy to begin with.
        """
        if not np.getPythonTag(TAG_MODEL_ROOT_CHILD):
            np.reparentTo(self.data)
            
    def GetFullPath(self, node):
        return MR.get_fullpath(node)
