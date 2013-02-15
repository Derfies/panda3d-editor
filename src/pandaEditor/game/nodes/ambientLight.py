import pandac.PandaModules as pm

from light import Light


class AmbientLight( Light ):
    
    def __init__( self, *args, **kwargs ):
        kwargs.setdefault( 'cType', pm.AmbientLight )
        Light.__init__( self, *args, **kwargs )