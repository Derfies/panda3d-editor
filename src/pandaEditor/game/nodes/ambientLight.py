import pandac.PandaModules as pm

from .light import Light


class AmbientLight( Light ):
    
    type_ = pm.AmbientLight