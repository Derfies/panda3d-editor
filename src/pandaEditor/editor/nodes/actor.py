import os

import pandac.PandaModules as pm

from constants import *
from game.nodes.actor import Actor as GameActor


class Actor( GameActor ):
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        wrpr = super( Actor, cls ).Create( *args, **kwargs )
        wrpr.data.setPythonTag( TAG_PICKABLE, True )
        return wrpr
    
    def GetCreateArgs( self ):
        return {'modelPath':self.GetRelModelPath( self.data.getPythonTag( 'modelPath' ) )}