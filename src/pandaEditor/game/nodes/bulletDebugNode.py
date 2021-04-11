from panda3d.bullet import BulletDebugNode as BDN

from game.nodes.manager import import_wrapper


TAG_BULLET_DEBUG_WIREFRAME = 'P3D_BulletDebugWireframe'


NodePath = import_wrapper('nodes.nodePath.NodePath')
Attr = import_wrapper('nodes.attributes.Attribute')


class BulletDebugNode(NodePath):
    
    type_ = BDN
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.AddAttributes(
            Attr('Show Wireframe', bool, self.GetWireframe, self.SetWireframe),
            parent='BulletDebugNode'
        )
        
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = super(BulletDebugNode, cls).Create(*args, **kwargs)
        wrpr.SetWireframe(wrpr.data, True)
        wrpr.data.show()
        return wrpr
        
    def GetWireframe(self, np):
        return np.getPythonTag(TAG_BULLET_DEBUG_WIREFRAME)
    
    def SetWireframe(self, np, val):
        np.node().showWireframe(val)
        np.setPythonTag(TAG_BULLET_DEBUG_WIREFRAME, val)
