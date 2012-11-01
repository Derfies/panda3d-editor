import os

import pandac.PandaModules as pm

from constants import *
from nodePath import NodePath
from attributes import NodeAttribute as Attr


class ModelRoot( NodePath ):
    
    def __init__( self, *args, **kwargs ):
        kwargs['nType'] = pm.ModelRoot
        NodePath.__init__( self, *args, **kwargs )
        
    def Create( self, modelPath='' ):
        filePath = pm.Filename.fromOsSpecific( modelPath )
        try:
            np = loader.loadModel( filePath )
        except:
            try:
                np = loader.loadModel( filePath + '.bam' )
            except IOError:
                print 'Failed to load: ', filePath
                np = pm.NodePath( pm.ModelRoot( '' ) )
        np.setName( filePath.getBasenameWoExtension() )
        
        # Iterate over child nodes
        def Recurse( node ):
            nTypeStr = node.getTag( TAG_NODE_TYPE )
            Wrpr = base.game.nodeMgr.GetWrapperByName( nTypeStr )
            if Wrpr is not None:
                wrpr = Wrpr( node )
                wrpr.Create( inputNp=node )
            
            # Recurse
            for child in node.getChildren():
                Recurse( child )
                
        Recurse( np )
        
        self.SetupNodePath( np )
        self.Wrap( np )
        
        return np
    
    def Wrap( self, np ):
        NodePath.Wrap( self, np )
        
        self.createArgs = {'modelPath':self.GetRelModelPath()}
    
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