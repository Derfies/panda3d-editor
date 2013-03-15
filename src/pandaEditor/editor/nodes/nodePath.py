import pandac.PandaModules as pm
from pandac.PandaModules import NodePath as NP
from direct.directtools.DirectSelection import DirectBoundingBox

from constants import *
from game.nodes.constants import *
from pandaEditor import commands as cmds
from game.nodes.nodePath import NodePath as GameNodePath
from game.nodes.attributes import NodePathAttribute as Attr


class NodePath( GameNodePath ):
    
    geo = None
    pickable = True
    
    def __init__( self, *args, **kwargs ):
        GameNodePath.__init__( self, *args, **kwargs )
        
        # Find the index of the 'name' property so we can add position, 
        # rotation and scale properties immediately after it.
        i = self.attributes.index( self.FindProperty( 'name' ) )
        
        # Add attributes for position, rotation and scale. These are 
        # implemented editor side only as we only need a matrix to xform the 
        # NodePath; they are for the user's benefit only.
        self.AddAttributes( Attr( 'Position', pm.Vec3, NP.getPos, NP.setPos, w=False ), index=i + 1 )
        self.AddAttributes( 
            Attr( 'X', float, NP.getX, NP.setX, w=False ),
            Attr( 'Y', float, NP.getY, NP.setY, w=False ),
            Attr( 'Z', float, NP.getZ, NP.setZ, w=False ),
            parent='Position'
        )
        
        self.AddAttributes( Attr( 'Rotation', pm.Vec3, NP.getHpr, NP.setHpr, w=False ), index=i + 2 )
        self.AddAttributes( 
            Attr( 'H', float, NP.getH, NP.setH, w=False ),
            Attr( 'P', float, NP.getP, NP.setP, w=False ),
            Attr( 'R', float, NP.getR, NP.setR, w=False ),
            parent='Rotation'
        )
        
        self.AddAttributes( Attr( 'Scale', pm.Vec3, NP.getScale, NP.setScale, w=False ), index=i + 3 )
        self.AddAttributes( 
            Attr( 'Sx', float, NP.getSx, NP.setSx, w=False ),
            Attr( 'Sy', float, NP.getSy, NP.setSy, w=False ),
            Attr( 'Sz', float, NP.getSz, NP.setSz, w=False ),
            parent='Scale'
        )
        
    @classmethod
    def SetPickable( cls, value=True ):
        cls.pickable = value
        
    @classmethod
    def SetEditorGeometry( cls, geo ):
        """
        Set the indicated geometry to be used as a proxy for the NodePath. 
        Tag all descendant NodePaths with the ignore tag so they don't show up
        in the scene graph and cannot be selected.
        """
        for childNp in geo.findAllMatches( '**' ):
            childNp.setPythonTag( TAG_IGNORE, True )
        geo.setLightOff()
        geo.node().adjustDrawMask( *base.GetEditorRenderMasks() )
        cls.geo = geo
        
    def SetupNodePath( self ):
        GameNodePath.SetupNodePath( self )
        
        if self.geo is not None:
            self.geo.copyTo( self.data )
            
        if self.pickable:
            self.data.setPythonTag( TAG_PICKABLE, self.pickable )
            
    def OnSelect( self ):
        """Add a bounding box to the indicated node."""
        bbox = DirectBoundingBox( self.data, (1, 1, 1, 1) )
        bbox.show()
        bbox.lines.setPythonTag( TAG_IGNORE, True )
        bbox.lines.node().adjustDrawMask( *base.GetEditorRenderMasks() )
        self.data.setPythonTag( TAG_BBOX, bbox )
        return bbox
    
    def OnDeselect( self ):
        """Remove the bounding box from the indicated node."""
        bbox = self.data.getPythonTag( TAG_BBOX )
        if bbox is not None:
            bbox.lines.removeNode()
        self.data.clearPythonTag( TAG_BBOX )
    
    def OnDelete( self, np ):
        pass
    
    def GetTags( self ):
        tags = self.data.getPythonTag( TAG_PYTHON_TAGS )
        if tags is not None:
            return [tag for tag in tags if tag in base.game.nodeMgr.nodeWrappers]
        
        return []
    
    def GetChildren( self ):
        children = []
        
        # Add wrappers for child NodePaths.
        for np in self.data.getChildren():
            if not np.getPythonTag( TAG_IGNORE ):
                children.append( base.game.nodeMgr.Wrap( np ) )
            
        return children
    
    def GetAddons( self ):
        children = []
        
        # Add wrappers for python objects.
        for tag in self.GetTags():
            pyObj = self.data.getPythonTag( tag )
            pyObjWrpr = base.game.nodeMgr.nodeWrappers[tag]
            children.append( pyObjWrpr( pyObj ) )
            
        return children
        
    def GetId( self ):
        return self.data.getTag( TAG_NODE_UUID )
    
    def SetId( self, id ):
        self.data.setTag( TAG_NODE_UUID, id )
    
    def GetParent( self ):
        return self.data.getParent()
    
    def GetName( self ):
        return self.data.getName()
    
    def GetCreateArgs( self ):
        args = GameNodePath.GetCreateArgs( self )
        
        # If this node is a child of a model root, make sure to add its
        # position in the hierarchy to the list of create arguments.
        if self.GetModified():
            modelRoot = self.data.findNetPythonTag( TAG_PICKABLE )
            
            def Rec( tgtNp, np, path ):
                if np.compareTo( tgtNp ) != 0:
                    path.insert( 0, np.getName() )
                    Rec( tgtNp, np.getParent(), path )
            
            path = []
            Rec( modelRoot, self.data, path )
            args['path'] = '|'.join( path )
            
        return args
    
    def GetModified( self ):
        return self.data.getPythonTag( TAG_MODIFIED )
    
    def SetModified( self, val ):
        if self.data.getPythonTag( TAG_MODEL_ROOT_CHILD ):
            self.data.setPythonTag( TAG_MODIFIED, val )
    
    def ValidateDragDrop( self, dragComps, dropComp ):
        dragNps = [dragComp for dragComp in dragComps if type( dragComp ) == pm.NodePath]
        if not dragNps:
            return False
        
        # If the drop item is none then the drop item will default to the
        # root node. No other checks necessary.
        if dropComp is None:
            return True
            
        # Fail if the drop item is one of the items being dragged
        #dropNp = dropItem.GetData()
        if dropComp in dragComps:
            return False
        
        # Fail if the drag items are ancestors of the drop items
        if True in [comp.isAncestorOf( dropComp ) for comp in dragComps]:
            return False
        
        # Drop target item is ok, continue
        return True
    
    def OnDragDrop( self, dragComps, dropNp ):
        dragNps = [dragComp for dragComp in dragComps if type( dragComp ) == pm.NodePath]
        if dragNps:
            cmds.Parent( dragNps, dropNp )
            
    def IsOfType( self, cType ):
        return self.data.node().isOfType( cType )
            
    def SetDefaultValues( self ):
        
        # Set default parent.
        self.data.reparentTo( render )
        
    def IsSaveable( self ):
        if self.data.getPythonTag( TAG_MODEL_ROOT_CHILD ):
            return self.GetModified()
        else:
            return True
        
    @classmethod
    def FindChild( cls, *args, **kwargs ):
        np = super( NodePath, cls ).FindChild( *args, **kwargs )
        np.setPythonTag( TAG_MODIFIED, True )
        return np