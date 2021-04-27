import panda3d.core as pc
from direct.showbase.PythonUtil import getBase as get_base

from game.nodes.attributes import Attribute
from game.nodes.constants import (
    TAG_MODEL_ROOT_CHILD, TAG_NODE_TYPE
)
from game.nodes.nodepath import NodePath


class ModelRoot(NodePath):
    
    type_ = pc.ModelRoot
    model_path = Attribute(
        pc.Filename,
        pc.ModelRoot.get_fullpath,
        init_arg='',
        node_data=True,
    )

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

        comp = super().create(data=np)
        
        # Iterate over child nodes
        # TBH I'm not even sure I know what this does.
        comp.extraNps = []
        def Recurse(node):
            nTypeStr = node.getTag(TAG_NODE_TYPE)
            cWrprCls = get_base().node_manager.get_component_by_name(nTypeStr)
            if cWrprCls is not None:
                cWrpr = cWrprCls.create(inputNp=node)
                comp.extraNps.append(cWrpr.data)
            
            # Recurse
            for child in node.getChildren():
                Recurse(child)
                
        Recurse(np)
        
        return comp
    
    def add_child(self, child):
        """
        Parent the indicated NodePath to the NodePath wrapped by this object.
        We don't have to parent NodePaths with the model root tag as they were
        created with the correct hierarchy to begin with.
        """
        if not child.data.get_python_tag(TAG_MODEL_ROOT_CHILD):
            child.data.reparent_to(self.data)
