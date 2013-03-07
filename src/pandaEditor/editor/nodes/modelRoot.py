import os

import pandac.PandaModules as pm

from constants import *
from game.nodes.constants import *
from game.nodes.modelRoot import ModelRoot as GameModelRoot


class ModelRoot( GameModelRoot ):
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        wrpr = GameModelRoot.Create( cls, *args, **kwargs )
        
        # Tag each descendant NodePath as a child of a model root. This edits
        # of these NodePaths to be saved out.
        for childNp in wrpr.data.findAllMatches( '**/*' ):
            childNp.setPythonTag( TAG_MODEL_ROOT_CHILD, True )
        
        return wrpr

    def GetCreateArgs( self ):
        return {'modelPath':self.GetRelModelPath( self.data.node().getFullpath() )}
    
    def GetRelModelPath( self, pandaPath ):
        """
        Attempt to find the indicated file path on one of the model search 
        paths. If found then return a path relative to it. Also make sure to 
        remove all extensions so we can load  both egg and bam files.
        """
        relPath = pm.Filename( pandaPath )
        index = relPath.findOnSearchpath( pm.getModelPath().getValue() )
        if index >= 0:
            basePath = pm.getModelPath().getDirectories()[index]
            relPath.makeRelativeTo( basePath )
            
        # Remove all extensions
        modelPath = str( relPath )
        while True:
            modelPath, ext = os.path.splitext( modelPath )
            if not ext:
                break
        
        return modelPath