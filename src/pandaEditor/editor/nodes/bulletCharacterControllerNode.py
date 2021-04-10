from panda3d.bullet import BulletWorld as BW

from pandaEditor.game.nodes.attributes import NodePathTargetConnectionList as CnnctnList
from pandaEditor.game.nodes.bulletCharacterControllerNode import BulletCharacterControllerNode as GameBulletCharacterControllerNode


class BulletCharacterControllerNode(GameBulletCharacterControllerNode):
    
    def SetDefaultValues(self):
        GameBulletCharacterControllerNode.SetDefaultValues(self)
        
        # Attempt to connect this node to the physics world if here is one.
        if base.scene.physicsWorld is not None:
            cnnctn = CnnctnList('Character', None, None, BW.attachCharacter, 
                                 None, BW.removeCharacter, 
                                 base.scene.physicsWorld)
            cnnctn.Connect(self.data)