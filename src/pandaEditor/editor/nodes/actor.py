import os

import pandac.PandaModules as pm

from constants import *
from game.nodes.actor import Actor as GameActor


class Actor( GameActor ):
        
    def Create( self, *args, **kwargs ):
        np = GameActor.Create( self, *args, **kwargs )
        np.setPythonTag( TAG_PICKABLE, True )
        return np
    
    def GetCreateArgs( self ):
        return {'modelPath':self.GetRelModelPath( self.data.getPythonTag( 'modelPath' ) )}