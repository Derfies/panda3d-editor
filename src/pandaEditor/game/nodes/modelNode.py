import pandac.PandaModules as pm

from nodePath import NodePath


class ModelNode( NodePath ):
    
    def __init__( self, *args, **kwargs ):
        kwargs['nType'] = pm.ModelNode
        NodePath.__init__( self, *args, **kwargs )