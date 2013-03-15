import pandac.PandaModules as pm

import p3d
import game
import nodes


class Scene( game.Scene ):
    
    def __init__( self, *args, **kwargs ):
        game.Scene.__init__( self, *args, **kwargs )
        
        self.cnnctns = {}
        
        self.filePath = kwargs.pop( 'filePath', None )
        p3d.Object.__init__( self, *args, **kwargs )
        self.rootNp.reparentTo( base.edRender )
        
        # Tag default nodes
        render.setTag( game.nodes.TAG_NODE_TYPE, 'Render' )
        base.cam.setTag( game.nodes.TAG_NODE_TYPE, 'BaseCam' )
        base.camera.setTag( game.nodes.TAG_NODE_TYPE, 'BaseCamera' )
        
        # Call create to run editor create methods.
        base.game.nodeMgr.Create( 'Render' )
        base.game.nodeMgr.Create( 'BaseCam' )
        base.game.nodeMgr.Create( 'BaseCamera' )
        
    def Load( self, **kwargs ):
        """Recreate a scene graph from file."""
        filePath = kwargs.get( 'filePath', self.filePath )
        if filePath is None:
            return False
        
        base.game.scnParser.Load( self.rootNp, filePath )
    
    def Save( self, **kwargs ):
        """Save a scene graph to file."""
        filePath = kwargs.get( 'filePath', self.filePath )
        if filePath is None:
            return False
        
        base.game.scnParser.Save( self, filePath )
        
    def Close( self ):
        """Destroy the scene by removing all its components."""
        def Destroy( wrpr ):
            for cWrpr in wrpr.GetChildren():
                Destroy( cWrpr )
            wrpr.Destroy()
            
        Destroy( base.game.nodeMgr.Wrap( self ) )
        base.game.pluginMgr.OnSceneClose()
        
        # Now remove the root node. If the root node was render, reset base
        # in order to remove and recreate the default node set.
        if self.rootNp is render:
            base.Reset()
        
        self.rootNp.removeNode()
    
    def DuplicateNodePaths( self, nps ):
        """Duplicate node paths."""
        dupeNps = []
        
        for np in nps:
            
            # Copy the node, parenting to the same parent as the original
            dupeNp = np.copyTo( np.getParent() )
            dupeNps.append( dupeNp )
        
            # Call duplicate methods for any wrappers
            wrpr = base.game.nodeMgr.Wrap( np )
            wrpr.Duplicate( np, dupeNp )
        
        return dupeNps