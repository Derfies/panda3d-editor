import panda3d.core as pc
from direct.showbase.PythonUtil import getBase as get_base

from game.nodes.attributes import Attribute
from game.nodes.constants import TAG_MODEL_ROOT_CHILD
from game.nodes.nodepath import NodePath


class ModelRoot(NodePath):
    
    type_ = pc.ModelRoot
    fullpath = Attribute(
        pc.Filename,
        pc.ModelRoot.get_fullpath,
        required=True,
        node_data=True,
    )

    @classmethod
    def create(cls, *args, **kwargs):
        fullpath = kwargs.pop('fullpath', None)
        if fullpath is not None:
            panda_fullpath = pc.Filename.from_os_specific(fullpath)
            np = get_base().loader.load_model(panda_fullpath)
            kwargs['data'] = np

        comp = super().create(*args, **kwargs)
        fullpath = comp.data.node().get_fullpath()
        comp.data.set_name(fullpath.get_basename_wo_extension())
        
        # Iterate over child nodes
        # TBH I'm not even sure I know what this does.
        # comp.extraNps = []
        # def Recurse(node):
        #     nTypeStr = node.getTag(TAG_NODE_TYPE)
        #     cWrprCls = get_base().node_manager.get_component_by_name(nTypeStr)
        #     if cWrprCls is not None:
        #         cWrpr = cWrprCls.create(inputNp=node)
        #         comp.extraNps.append(cWrpr.data)
        #
        #     # Recurse
        #     for child in node.getChildren():
        #         Recurse(child)
        #
        # Recurse(comp.data)
        
        return comp
    
    def add_child(self, child):
        """
        Parent the indicated NodePath to the NodePath wrapped by this object.
        We don't have to parent NodePaths with the model root tag as they were
        created with the correct hierarchy to begin with.
        """
        if not child.data.get_python_tag(TAG_MODEL_ROOT_CHILD):
            child.data.reparent_to(self.data)
