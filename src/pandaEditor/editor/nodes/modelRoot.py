import os

from constants import *
import pandac.PandaModules as pm

from game.nodes.modelRoot import ModelRoot as GameModelRoot


class ModelRoot( GameModelRoot ):
    
    def Create( self, *args, **kwargs ):
        np = GameModelRoot.Create( self, *args, **kwargs )
        
        # Tag child nodes so they don't get saved out. This is a hack fix to
        # a larger problem - we need to be able to save / load child node
        # transforms and properties eventually.
        for child in np.getChildren():
            child.setPythonTag( TAG_DO_NOT_SAVE, True )
        
        return np

    def GetCreateArgs( self ):
        return {'modelPath':self.GetRelModelPath()}
    
    def GetRelModelPath( self ):
        """
        Attempt to find the indicated file path on one of the model search 
        paths. If found then return a path relative to it. Also make sure to 
        remove all extensions so we can load  both egg and bam files.
        """
        node = self.data.node()
        
        relPath = pm.Filename( node.getFullpath() )
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