import pandac.PandaModules as pm

from .lensNode import LensNode


class Camera( LensNode ):
    
    type_ = pm.Camera
    
    def __init__( self, *args, **kwargs ):
        LensNode.__init__( self, *args, **kwargs )