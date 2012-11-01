import pandac.PandaModules as pm

from constants import *
from game.nodes.lensNode import LensNode as GameLensNode


class LensNode( GameLensNode ):
    
    def OnSelect( self, np ):
        children = set( np.getChildren() )
        np.node().showFrustum()
        frustum = list( set( np.getChildren() ) - children )[0]
        frustum.setPythonTag( TAG_IGNORE, True )
        
    def OnDeselect( self, np ):
        np.node().hideFrustum()