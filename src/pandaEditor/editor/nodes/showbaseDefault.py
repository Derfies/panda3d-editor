from constants import *
from game.nodes.showbaseDefault import *
from game.nodes.showbaseDefault import Render as GameRender
from game.nodes.showbaseDefault import Render2d as GameRender2d
from game.nodes.showbaseDefault import Aspect2d as GameAspect2d


class Render( GameRender ):
    
    def GetParent( self ):
        return base.game.nodeMgr.Wrap( base.scene )
    

class Render2d( GameRender2d ):
    
    def GetParent( self ):
        return base.game.nodeMgr.Wrap( base.scene )
    

class Aspect2d( GameAspect2d ):
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        wrpr = super( Aspect2d, cls ).Create( *args, **kwargs )
        
        # Tag all NodePaths under this node with the ignore tag. They are used
        # to help caculate the aspect ratio and don't need to be saved out or
        # edited. As long as this NodePath wrapper is created before parenting
        # any other NodePaths the user may have created we shouldn't get into
        # much trouble.
        for childNp in wrpr.data.getChildren():
            childNp.setPythonTag( TAG_IGNORE, True )
        return wrpr