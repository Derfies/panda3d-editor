import pandac.PandaModules as pm

import p3d
from constants import *
from nodePath import NodePath
from attributes import Attribute


class Actor( NodePath ):
    
    def __init__( self, *args, **kwargs ):
        NodePath.__init__( self, *args, **kwargs )
        
        self.attributes.append( Attribute( 'Actor' ) )
        
    def Create( self, filePath ):
        filePath = pm.Filename.fromOsSpecific( filePath )
        try:
            np = loader.loadModel( filePath )
        except:
            np = loader.loadModel( filePath + '.bam' )
    
        pObj = p3d.PandaObject( np )
        pObj.CreateActor()
        np.removeNode()
        np = pObj.np
        
        np.setTag( TAG_NODE_TYPE, 'Actor' )
        
        return np