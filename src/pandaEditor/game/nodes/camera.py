import pandac.PandaModules as pm

from lensNode import LensNode


class Camera( LensNode ):
    
    def __init__( self, *args, **kwargs ):
        kwargs['nType'] = pm.Camera
        LensNode.__init__( self, *args, **kwargs )