import os

import pandac.PandaModules as pm

from constants import *
from nodePath import NodePath
from attributes import NodeAttribute as Attr


class ModelRoot( NodePath ):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'cType', pm.ModelRoot )
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
        #np.reparentTo( parent )
        
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
        self.data = np
        
        return np