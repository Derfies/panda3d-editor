import panda3d.core as pc
from direct.showbase.PythonUtil import getBase as get_base
#from panda3d.core import ModelRoot as MR

from game.nodes.attributes import Attribute, NodeAttribute
from game.nodes.constants import (
    TAG_MODEL_ROOT_CHILD, TAG_NODE_TYPE
)
from game.nodes.nodepath import NodePath
from game.nodes.othermeta import ComponentMetaClass


class ModelPathAttribute(Attribute, metaclass=ComponentMetaClass):

    @property
    def value(self):
        return pc.ModelRoot.get_fullpath(self.data.node())


class ModelRoot(NodePath):
    
    type_ = pc.ModelRoot
    model_path = ModelPathAttribute(pc.Filename, init_arg='')

    @classmethod
    def create(cls, *args, **kwargs):
        model_path = kwargs.pop('model_path', '')
        if not model_path:
            np = pc.NodePath(pc.ModelRoot(''))
        else:
            filePath = pc.Filename.fromOsSpecific(model_path)
            try:
                np = get_base().loader.loadModel(filePath)
            except:
                try:
                    np = get_base().loader.loadModel(filePath + '.bam')
                except IOError:
                    print('Failed to load: ', filePath)
                    np = pc.NodePath(pc.ModelRoot(''))
            np.setName(filePath.getBasenameWoExtension())
        
        comp = cls(np)
        comp.set_up_node_path()
        
        # Iterate over child nodes
        comp.extraNps = []
        def Recurse(node):
            nTypeStr = node.getTag(TAG_NODE_TYPE)
            cWrprCls = get_base().node_manager.GetWrapperByName(nTypeStr)
            if cWrprCls is not None:
                cWrpr = cWrprCls.create(inputNp=node)
                comp.extraNps.append(cWrpr.data)
            
            # Recurse
            for child in node.getChildren():
                Recurse(child)
                
        Recurse(np)
        
        return comp
    
    def add_child(self, np):
        """
        Parent the indicated NodePath to the NodePath wrapped by this object.
        We don't have to parent NodePaths with the model root tag as they were
        created with the correct hierarchy to begin with.
        """
        if not np.get_python_tag(TAG_MODEL_ROOT_CHILD):
            np.reparent_to(self.data)

