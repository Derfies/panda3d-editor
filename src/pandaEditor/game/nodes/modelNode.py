import pandac.PandaModules as pm

from nodePath import NodePath


class ModelNode( NodePath ):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'cType', pm.ModelNode )
        NodePath.__init__( self, *args, **kwargs )