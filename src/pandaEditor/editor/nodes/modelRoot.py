import os

import pandac.PandaModules as pm

from constants import *
from game.nodes.constants import *
from game.nodes.modelRoot import ModelRoot as GameModelRoot


class ModelRoot( GameModelRoot ):
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        wrpr = super( ModelRoot, cls ).Create( *args, **kwargs )
        
        # Tag each descendant NodePath as a child of a model root. This edits
        # of these NodePaths to be saved out.
        for childNp in wrpr.data.findAllMatches( '**/*' ):
            childNp.setPythonTag( TAG_MODEL_ROOT_CHILD, True )
        
        return wrpr
    
    def GetFullPath( self, node ):
        relPath = base.project.GetRelModelPath( node.getFullpath() )
        return relPath