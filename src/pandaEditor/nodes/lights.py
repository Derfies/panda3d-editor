import panda3d.core as pc

from game.nodes.attributes import ConnectionList


class Light:
    
    def SetDefaultValues(self):
        super().SetDefaultValues()

        cnnctn = ConnectionList(
            'Lights',
            pc.Light,
            self.GetLights,
            pc.NodePath.set_light,
            pc.NodePath.clear_light,
            pc.NodePath.clear_light,
            base.scene.rootNp
        )
        cnnctn.Connect(self.data)
