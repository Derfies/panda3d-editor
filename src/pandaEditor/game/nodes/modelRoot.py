import os

import pandac.PandaModules as pm

from constants import *
from nodePath import NodePath
from attributes import NodeAttribute as Attr


class ModelRoot( NodePath ):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'cType', pm.ModelRoot )
        NodePath.__init__( self, *args, **kwargs )
        
    def Create( self, *args, **kwargs ):
        modelPath = kwargs['modelPath']
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
            wrprCls = base.game.nodeMgr.GetWrapperByName( nTypeStr )
            if wrprCls is not None:
                wrpr = wrprCls( node )
                wrpr.Create( inputNp=node )
            
            # Recurse
            for child in node.getChildren():
                Recurse( child )
                
        Recurse( np )
        
        self.SetupNodePath( np )
        self.data = np
        
        return np
    
    def AddChild( self, np ):
        """
        Parent the indicated NodePath to the NodePath wrapped by this object.
        We don't have to parent NodePaths with the model root tag as they were
        created with the correct hierarchy to begin with.
        """
        if not np.getPythonTag( TAG_MODEL_ROOT_CHILD ):
            np.reparentTo( self.data )