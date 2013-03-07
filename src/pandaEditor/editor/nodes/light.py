import pandac.PandaModules as pm
from pandac.PandaModules import NodePath as NP

from game.nodes.light import Light as GameLight
from game.nodes.attributes import ConnectionList as CnnctnL


class Light( GameLight ):
    
    def SetDefaultValues( self ):
        GameLight.SetDefaultValues( self )
        
        cnnctn = CnnctnL( 'Light', pm.Light, self.GetLights, NP.setLight, NP.clearLight, NP.clearLight, base.scene.rootNp )
        cnnctn.Connect( self.data )