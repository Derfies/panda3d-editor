import os

import pandac.PandaModules as pm

from constants import *
from nodePath import NodePath
from attributes import NodeAttribute as Attr


class ModelRoot( NodePath ):
    
    type_ = pm.ModelRoot
    
    @classmethod
    def Create( cls, *args, **kwargs ):
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
                wrprCls.Create( inputNp=node )
            
            # Recurse
            for child in node.getChildren():
                Recurse( child )
                
        Recurse( np )
        
        wrpr = cls( np )
        wrpr.SetupNodePath()
        
        return wrpr
    
    def AddChild( self, np ):
        """
        Parent the indicated NodePath to the NodePath wrapped by this object.
        We don't have to parent NodePaths with the model root tag as they were
        created with the correct hierarchy to begin with.
        """
        if not np.getPythonTag( TAG_MODEL_ROOT_CHILD ):
            np.reparentTo( self.data )