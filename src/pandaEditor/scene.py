import copy

import pandac.PandaModules as pm

import p3d
import game
import editor


class Scene( p3d.Object ):
    
    def __init__( self, app, *args, **kwargs ):
        self.app = app
        
        self.filePath = kwargs.pop( 'filePath', None )
        p3d.Object.__init__( self, *args, **kwargs )
        
        # Tag default nodes
        base.cam.setTag( game.nodes.TAG_NODE_TYPE, 'BaseCam' )
        base.camera.setTag( game.nodes.TAG_NODE_TYPE, 'BaseCamera' )
        
        # Call create to run editor create methods.
        base.game.nodeMgr.Create( 'BaseCam' )
        base.game.nodeMgr.Create( 'BaseCamera' )
        
    def Load( self, **kwargs ):
        """Recreate a scene graph from file."""
        filePath = kwargs.get( 'filePath', self.filePath )
        if filePath is None:
            return False
        
        self.app.game.scnParser.Load( self.rootNp, filePath )
    
    def Save( self, **kwargs ):
        """Save a scene graph to file."""
        filePath = kwargs.get( 'filePath', self.filePath )
        if filePath is None:
            return False
        
        self.app.game.scnParser.Save( self.rootNp, filePath )
        
    def Close( self ):
        """Destroy the scene by removing all its nodes."""
        def Destroy( np, cookie ):
            wrpr = base.game.nodeMgr.Wrap( np )
            if wrpr is not None:
                wrpr.Destroy()
        
        self.Walk( Destroy )
        self.app.game.pluginMgr.OnSceneClose()
        
        # Now remove the root node. If the root node was render, reset base
        # in order to remove and recreate the default node set.
        if self.rootNp is render:
            base.Reset()
            
            # Reset references to render
            self.app.selection.marquee.rootNp = render
        
        self.rootNp.removeNode()
        
    def AddNodePaths( self, nps ):
        """Parent the indicated node paths to the scene root."""
        for np in nps:
            np.reparentTo( self.rootNp )
        
    def DeleteNodePaths( self, nps ):
        """
        Delete the indicated node paths. Remember to call OnDelete methods on
        the node wrapper.
        """
        for np in nps:
            
            # Call delete methods for any wrappers
            wrpr = base.game.nodeMgr.Wrap( np )
            if wrpr is not None:
                wrpr.OnDelete( np )
                
            np.detachNode()
    
    def DuplicateNodePaths( self, nps ):
        """Duplicate node paths."""
        dupeNps = []
        
        for np in nps:
            
            # Copy the node, parenting to the same parent as the original
            dupeNp = np.copyTo( np.getParent() )
            dupeNps.append( dupeNp )
        
            # Call duplicate methods for any wrappers
            wrpr = base.game.nodeMgr.Wrap( np )
            if wrpr is not None:
                wrpr.Duplicate( np, dupeNp )
        
        return dupeNps
        
    def Walk( self, func, np=None, arg=None, includeHelpers=False, modelRootsOnly=True ):
        """Walk hierarchy calling func on each member."""
        if np is None:
            np = self.rootNp
        
        # Bail if helpers were not included and this node represents a helper
        # geometry or collision
        if not includeHelpers and np.getPythonTag( editor.nodes.TAG_IGNORE ):
            return
        
        children = np.getChildren()
        func( np, arg )
        
        # Flag as being under a model root before processing children.
        # WARNING: this may play badly with eggs that have nested children.
        isActor = False
        pObj = p3d.PandaObject.Get( np )
        if pObj is not None and hasattr( pObj, 'actor' ) and pObj.actor:
            isActor = True
            self.underModelRoot = True
            
        isModelRoot = np.node().isOfType( pm.ModelRoot )
        if isModelRoot:
            self.underModelRoot = True
        
        if not modelRootsOnly or ( modelRootsOnly and not 
                                   np.node().isOfType( pm.ModelRoot ) ):
            for child in children:
                self.Walk( func, child, arg, includeHelpers, modelRootsOnly )
                
        # Finished processing children - reset underModelRoot flag.
        if isModelRoot or isActor:
            self.underModelRoot = False