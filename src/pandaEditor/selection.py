import pandac.PandaModules as pm

import p3d
import editor


class Selection( p3d.Object ):
    
    BBOX_TAG = 'bbox'
    
    def __init__( self, *args, **kwargs ):
        p3d.Object.__init__( self, *args, **kwargs )
        
        self.nps = []
        
        # Create a marquee
        self.marquee = p3d.Marquee( 'marquee', *args, **kwargs )
        
        # Create node picker - set its collision mask to hit both geom nodes
        # and collision nodes
        bitMask = pm.GeomNode.getDefaultCollideMask() | pm.CollisionNode.getDefaultCollideMask()
        self.picker = p3d.MousePicker( 'picker', *args, fromCollideMask=bitMask, **kwargs )
        self.picker.Start()
        
    def Get( self ):
        """Return the selected node paths."""
        return self.nps
    
    def Clear( self ):
        """Clear the selection list and run deselect handlers."""
        for np in self.nps:
            #if not np.isEmpty():
            wrpr = base.game.nodeMgr.Wrap( np )
            wrpr.OnDeselect( np )
        self.nps = []
    
    def Add( self, nps ):
        """
        Add the indicated node paths to the selection and run select handlers.
        """
        for np in list( set( nps ) ):
            wrpr = base.game.nodeMgr.Wrap( np )
            wrpr.OnSelect( np )
                
            self.nps.append( np )
    
    def Remove( self, nps ):
        """
        Remove those node paths that were in the selection and run deselect
        handlers.
        """
        for np in nps:
            wrpr = base.game.nodeMgr.Wrap( np )
            wrpr.OnDeselect( np )
            
        self.nps = list( set( self.nps ) - set( nps ) )
    
    def SelectParent( self ):
        """Select parent node paths."""
        nps = []
        for np in self.nps:
            if np.getParent() != render:
                nps.append( np.getParent() )
            else:
                nps.append( np )
        return nps
        
    def SelectChild( self ):
        """Select child node paths."""
        nps = []
        for np in self.nps:
            children = np.getChildren()
            isIgnore = [child.getPythonTag( editor.nodes.TAG_IGNORE ) for child in children]
            if children and not isIgnore[0]:
                nps.append( children[0] )
            else:
                nps.append( np )
        return nps
            
    def SelectPrev( self ):
        """Select previous node paths."""
        nps = []
        for np in self.nps:
            
            # Find where the child appears in the list
            children = list( np.getParent().getChildren() )
            index = children.index( np ) - 1
            
            # Wrap around if the index has gone below zero
            if index < 0:
                index = len( children ) - 1
            
            nps.append( children[index] )
        return nps
        
    def SelectNext( self ):
        """Select next node paths."""
        nps = []
        for np in self.nps:
            
            # Find where the child appears in the list
            children = list( np.getParent().getChildren() )
            index = children.index( np ) + 1
            
            # Wrap around if the index has gone below zero
            if index > len( children ) - 1:
                index = 0
            
            nps.append( children[index] )
        return nps
    
    def StartDragSelect( self, append=False ):
        """
        Start the marquee and put the tool into append mode if specified.
        """
        if self.marquee.mouseWatcherNode.hasMouse():
            self.append = append
            self.marquee.Start()
    
    def StopDragSelect( self ):
        """
        Stop the marquee and get all the node paths under it with the correct
        tag. Also append any node which was under the mouse at the end of the
        operation.
        """
        nps = []
        
        # Stop the marquee
        self.marquee.Stop()
        
        # Find all node paths below the root node which are inside the marquee
        # AND have the correct tag
        for np in self.rootNp.findAllMatches( '**' ):
            if ( self.marquee.IsNodePathInside( np ) and
                 np.getPythonTag( editor.nodes.TAG_PICKABLE ) ):
                nps.append( np )
                    
        # Add any node path which was under the mouse to the selection
        np = self.GetNodePathUnderMouse()
        if np is not None:
            nps.append( np )
        
        # In append mode we want to add / remove items from the current
        # selection
        if self.append:
            for selfNp in self.nps:
                if selfNp in nps:
                    nps.remove( selfNp )
                else:
                    nps.append( selfNp )
        
        # Clear current selection and select new node paths
        return nps
        
    def GetNodePathUnderMouse( self ):
        """
        Returns the closest node under the mouse, or None if there isn't one.
        """
        pickedNp = self.picker.GetFirstNodePath()
        if pickedNp is not None:
            return pickedNp.findNetPythonTag( editor.nodes.TAG_PICKABLE )
        else:
            return None
        
    def Update( self ):
        """Update the selection by running deselect and select handlers."""
        for np in self.nps:
            wrpr = base.game.nodeMgr.Wrap( np )
            wrpr.OnDeselect( np )
            wrpr.OnSelect( np )