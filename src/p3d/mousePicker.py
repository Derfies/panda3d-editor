from pandac.PandaModules import CollisionTraverser, CollisionHandlerQueue, BitMask32
from pandac.PandaModules import CollisionNode, CollisionRay

import p3d


class MousePicker( p3d.SingleTask ):
    
    """
    Class to represent a ray fired from the input camera lens using the mouse.
    """
    
    def __init__( self, *args, **kwargs ):
        p3d.SingleTask.__init__( self, *args, **kwargs )
        
        self.fromCollideMask = kwargs.pop( 'fromCollideMask', None )
        
        self.node = None
        self.collEntry = None
        
        # Create collision nodes
        self.collTrav = CollisionTraverser()
        #self.collTrav.showCollisions( render )
        self.collHandler = CollisionHandlerQueue()
        self.pickerRay = CollisionRay()
        
        # Create collision ray
        pickerNode = CollisionNode( self.name )
        pickerNode.addSolid( self.pickerRay )
        pickerNode.setIntoCollideMask( BitMask32.allOff() )
        pickerNp = self.camera.attachNewNode( pickerNode )
        self.collTrav.addCollider( pickerNp, self.collHandler )
        
        # Create collision mask for the ray if one is specified
        if self.fromCollideMask is not None:
            pickerNode.setFromCollideMask( self.fromCollideMask )
        
        # Bind mouse button events
        eventNames = ['mouse1', 'control-mouse1', 'mouse1-up']
        for eventName in eventNames:
            self.accept( eventName, self.FireEvent, [eventName] )
    
    def OnUpdate( self, task, x=None, y=None ):
        
        # Update the ray's position
        if self.mouseWatcherNode.hasMouse():
            mp = self.mouseWatcherNode.getMouse()
            x, y = mp.getX(), mp.getY()
        if x is None or y is None:
            return
        self.pickerRay.setFromLens( self.camera.node(), x, y )
        
        # Traverse the hierarchy and find collisions
        self.collTrav.traverse( self.rootNp )
        if self.collHandler.getNumEntries():
            
            # If we have hit something, sort the hits so that the closest is first
            self.collHandler.sortEntries()
            collEntry = self.collHandler.getEntry( 0 )
            node = collEntry.getIntoNode()
            
            # If this node is different to the last node, send a mouse leave
            # event to the last node, and a mouse enter to the new node
            if node != self.node:
                if self.node is not None:
                    messenger.send( '%s-mouse-leave' % self.node.getName(), [self.collEntry] )
                messenger.send( '%s-mouse-enter' % node.getName(), [collEntry] )
            
            # Send a message containing the node name and the event over name,
            # including the collision entry as arguments
            messenger.send( '%s-mouse-over' % node.getName(), [collEntry] )
            
            # Keep these values
            self.collEntry = collEntry
            self.node = node
            
        elif self.node is not None:
            
            # No collisions, clear the node and send a mouse leave to the last
            # node that stored
            messenger.send( '%s-mouse-leave' % self.node.getName(), [self.collEntry] )
            self.node = None
            
    def FireEvent( self, event ):
        """
        Send a message containing the node name and the event name, including
        the collision entry as arguments.
        """
        if self.node is not None:
            messenger.send( '%s-%s' % ( self.node.getName(), event ), [self.collEntry] )
            
    def GetFirstNodePath( self ):
        """
        Return the first node in the collision queue if there is one, None
        otherwise.
        """
        if self.collHandler.getNumEntries():
            collEntry = self.collHandler.getEntry( 0 )
            return collEntry.getIntoNodePath()
        
        return None 