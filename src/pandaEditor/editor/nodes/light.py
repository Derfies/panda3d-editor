import pandac.PandaModules as pm

from constants import *
from game.nodes.light import Light as GameLight


class Light( GameLight ):
    
    def OnDelete( self, np ):
        """
        Make sure to clear the light from every NodePath in the scene or else
        it won't be properly removed.
        """
        for child in base.scene.rootNp.findAllMatches( '**' ):
            child.clearLight( np )