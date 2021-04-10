import panda3d.core as pm

import p3d
import game
from . import nodes


class Scene( game.Scene ):
    
    def __init__( self, *args, **kwargs ):
        game.Scene.__init__( self, *args, **kwargs )
        
        self.cnnctns = {}
        
        # 'Create' the default NodePaths that come from showbase. Calling the
        # create method in this way doesn't generate any new NodePaths, it
        # will simply return those the default showbase creates when it starts
        # up. Tag them so their type is overriden and the component manager
        # wraps them appropriately.
        defaultCompTypes = [
            'Render',
            'BaseCamera',
            'BaseCam',
            'Render2d',
            'Aspect2d',
            'Pixel2d',
            'Camera2d',
            'Cam2d'          
        ]
        for cType in defaultCompTypes:
            wrpr = base.game.nodeMgr.Create( cType )
            wrpr.data.setTag( game.nodes.TAG_NODE_TYPE, cType )
        
    def Load( self, filePath ):
        """Recreate a scene graph from file."""
        base.game.scnParser.Load( self.rootNp, filePath )
    
    def Save( self, filePath ):
        """Save a scene graph to file."""
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
        
    def GetOutgoingConnections( self, wrpr ):
        """
        Return all outgoing connections for the indicated component wrapper.
        """
        outCnnctns = []
        
        id = wrpr.GetId()
        if id in self.cnnctns:
            outCnnctns.extend( self.cnnctns[id] )
        
        return outCnnctns
    
    def GetIncomingConnections( self, wrpr ):
        """
        Return all incoming connections for the indicated component wrapper.
        """
        incCnnctns = []
        
        for id, cnnctns in self.cnnctns.items():
            for cnnctn in cnnctns:
                if cnnctn.srcComp == wrpr.data:
                    incCnnctns.append( cnnctn )
        
        return incCnnctns
    
    def RegisterConnection( self, comp, cnnctn ):
        """
        Register a connection to its target component. This allows us to find
        a connection and break it when a component is deleted.
        """
        compId = base.game.nodeMgr.Wrap( comp ).GetId()
        self.cnnctns.setdefault( compId, [] )
        cnnctnLabels = [cnnctn.label for cnnctn in self.cnnctns[compId]]
        if cnnctn.label not in cnnctnLabels:
            self.cnnctns[compId].append( cnnctn )
    
    def DeregisterConnection( self, comp, cnnctn ):
        compId = base.game.nodeMgr.Wrap( comp ).GetId()
        if compId in self.cnnctns:
            del self.cnnctns[compId]
        
    def ClearConnections( self, comp ):
        delIds = []
        for id, cnnctns in self.cnnctns.items():
            
            delCnnctns = []
            for cnnctn in cnnctns:
                if cnnctn.srcComp == comp:
                    delCnnctns.append( cnnctn )
                    
            for delCnnctn in delCnnctns:
                cnnctns.remove( delCnnctn )
                
            if not cnnctns:
                delIds.append( id )
                
        for delId in delIds:
            del self.cnnctns[delId]