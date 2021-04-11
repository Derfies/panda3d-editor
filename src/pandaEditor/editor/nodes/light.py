import panda3d.core as pm
from panda3d.core import NodePath as NP

from game.nodes.attributes import ConnectionList as CnnctnL
from game.nodes.light import Light as GameLight


class Light(GameLight):
    
    def SetDefaultValues(self):
        super().SetDefaultValues()
        
        cnnctn = CnnctnL('Lights', pm.Light, self.GetLights, NP.setLight, NP.clearLight, NP.clearLight, base.scene.rootNp)
        cnnctn.Connect(self.data)
