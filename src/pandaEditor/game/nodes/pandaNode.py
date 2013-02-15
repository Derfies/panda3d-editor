import pandac.PandaModules as pm

from nodePath import NodePath


class PandaNode( NodePath ):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'cType', pm.PandaNode )
        NodePath.__init__( self, *args, **kwargs )