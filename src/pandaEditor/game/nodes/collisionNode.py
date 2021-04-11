from panda3d.core import CollisionNode as CN, CollisionSolid as CS

from game.nodes.manager import import_wrapper


NodePath = import_wrapper('nodes.nodePath.NodePath')
Attr = import_wrapper('nodes.attributes.Attribute')
Cnnctn = import_wrapper('nodes.attributes.Cnnctn')


class CollisionNode(NodePath):
    
    type_ = CN
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.AddAttributes(
            Attr('Num Solids', int, CN.getNumSolids),
            Cnnctn('Solids', CS, CN.getSolids, CN.addSolid, CN.clearSolids, self.RemoveSolid, self.data),
            parent='CollisionNode'
       )
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = super(CollisionNode, cls).Create(*args, **kwargs)
        wrpr.data.show()
        return wrpr
    
    def RemoveSolid(self, srcComp, tgtComp):
        solids = srcComp.getSolids()
        index = solids.index(tgtComp)
        CN.removeSolid(srcComp, index)
