import pandac.PandaModules as pm

import p3d
import editor


class Selection( p3d.Object ):
    
    BBOX_TAG = 'bbox'
    
    def __init__( self, *args, **kwargs ):
        p3d.Object.__init__( self, *args, **kwargs )
        
        self.comps = []
        self.wrprs = []
        
        # Create a marquee
        self.marquee = p3d.Marquee( 'marquee', *args, **kwargs )
        
        # Create node picker - set its collision mask to hit both geom nodes
        # and collision nodes
        bitMask = pm.GeomNode.getDefaultCollideMask() | pm.CollisionNode.getDefaultCollideMask()
        self.picker = p3d.MousePicker( 'picker', *args, fromCollideMask=bitMask, **kwargs )
                
    def Get( self ):
        """Return the selected components."""
        return self.comps
    
    def GetNodePaths( self ):
        nps = [
            wrpr.data 
            for wrpr in self.wrprs
            if type( wrpr.data  ) == pm.NodePath
        ]
        return nps
    
    def Clear( self ):
        """Clear the selection list and run deselect handlers."""
        for wrpr in self.wrprs:
            wrpr.OnDeselect()
        self.comps = []
        self.wrprs = []
    
    def Add( self, comps ):
        """
        Add the indicated components to the selection and run select handlers.
        """
        for comp in list( set( comps ) ):
            wrpr = base.game.nodeMgr.Wrap( comp )
            wrpr.OnSelect()
                
            self.comps.append( comp )
            self.wrprs.append( wrpr )
    
    def Remove( self, comps ):
        """
        Remove those components that were in the selection and run deselect
        handlers.
        """
        for wrpr in self.wrprs:
            wrpr.OnDeselect()
            
        self.comps = list( set( self.comps ) - set( comps ) )
        self.wrprs = [base.game.nodeMgr.Wrap( comp ) for comp in self.comps]
    
    def SelectParent( self ):
        """
        Return a list of parent components from the selection. Include the
        original component if no suitable parent is found.
        """
        comps = []
        for wrpr in self.wrprs:
            pWrpr = wrpr.GetParent()
            if pWrpr.data != base.scene:
                comps.append( pWrpr.data )
            else:
                comps.append( wrpr.data )
        return comps
        
    def SelectChild( self ):
        """
        Return a list of child components from the selection. Include the
        original component if no children are found.
        """
        comps = []
        for wrpr in self.wrprs:
            cWrprs = wrpr.GetChildren()
            if cWrprs:
                comps.append( cWrprs[0].data )
            else:
                comps.append( wrpr.data )
        return comps
            
    def SelectPrev( self ):
        """
        For each component in the selection, return the component that appears
        one before in the parent's list of children. 
        """
        comps = []
        for wrpr in self.wrprs:
            pWrpr = wrpr.GetParent()
            cComps = [cWrpr.data for cWrpr in pWrpr.GetChildren()]
                
            # Get the index of the child before this one - wrap around if the 
            # index has gone below zero.
            index = cComps.index( wrpr.data ) - 1
            if index < 0:
                index = len( cComps ) - 1
            
            comps.append( cComps[index] )
        return comps
        
    def SelectNext( self ):
        """
        For each component in the selection, return the component that appears
        one after in the parent's list of children. 
        """
        comps = []
        for wrpr in self.wrprs:
            pWrpr = wrpr.GetParent()
            cComps = [cWrpr.data for cWrpr in pWrpr.GetChildren()]
            
            # Get the index of the child after this one - wrap around if the 
            # index has gone over the number of children.
            index = cComps.index( wrpr.data ) + 1
            if index > len( cComps ) - 1:
                index = 0
            
            comps.append( cComps[index] )
        return comps
    
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
            if self.marquee.IsNodePathInside( np ):
                nps.append( self.GetPickedNodePath( np ) )
                    
        # Add any node path which was under the mouse to the selection
        np = self.GetNodePathUnderMouse()
        if np is not None:
            nps.append( np )
        
        # In append mode we want to add / remove items from the current
        # selection
        if self.append:
            for selfNp in self.comps:
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
        self.picker.OnUpdate( None )
        pickedNp = self.picker.GetFirstNodePath()
        if pickedNp is not None:
            return self.GetPickedNodePath( pickedNp )
        else:
            return None
        
    def GetNodePathAtPosition( self, x, y ):
        self.picker.OnUpdate( None, x, y )
        pickedNp = self.picker.GetFirstNodePath()
        if pickedNp is not None:
            return self.GetPickedNodePath( pickedNp )
        else:
            return None
        
    def GetPickedNodePath( self, np ):
        if np.getPythonTag( editor.nodes.TAG_IGNORE ):
            return np.findNetPythonTag( editor.nodes.TAG_PICKABLE )
        elif p3d.MOUSE_CTRL in base.edCamera.mouse.modifiers:
            return np
        else:
            return np.findNetPythonTag( editor.nodes.TAG_PICKABLE )
        
    def Update( self ):
        """Update the selection by running deselect and select handlers."""
        for wrpr in self.wrprs:
            wrpr.OnDeselect()
            wrpr.OnSelect()