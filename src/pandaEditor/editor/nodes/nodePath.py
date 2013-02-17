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
        pAttr = self.FindProperty( 'nodePath' )
        index = pAttr.children.index( self.FindProperty( 'name' ) )
        
        # Add attributes for position, rotation and scale. These are
        # implemented editor side only as we only need a matrix to xform the
        # node. These are provided for the user's benefit only.
        attr = Attr( 'Position', pm.Vec3, NP.getPos, NP.setPos, w=False )
        attr.children.extend( 
            [
                Attr( 'X', float, NP.getX, NP.setX, w=False ),
                Attr( 'Y', float, NP.getY, NP.setY, w=False ),
                Attr( 'Z', float, NP.getZ, NP.setZ, w=False )
            ]
        )
        pAttr.children.insert( index + 1, attr )
        
        attr = Attr( 'Rotation', pm.Vec3, NP.getHpr, NP.setHpr, w=False )
        attr.children.extend( 
            [
                Attr( 'H', float, NP.getH, NP.setH, w=False ),
                Attr( 'P', float, NP.getP, NP.setP, w=False ),
                Attr( 'R', float, NP.getR, NP.setR, w=False )
            ]
        )
        pAttr.children.insert( index + 2, attr )
         
        attr = Attr( 'Scale', pm.Vec3, NP.getScale, NP.setScale, w=False )
        attr.children.extend( 
            [
                Attr( 'Sx', float, NP.getSx, NP.setSx, w=False ),
                Attr( 'Sy', float, NP.getSy, NP.setSy, w=False ),
                Attr( 'Sz', float, NP.getSz, NP.setSz, w=False )
            ]
        )
        pAttr.children.insert( index + 3, attr )
        
    @classmethod
    def SetPickable( cls, value=True ):
        cls.pickable = value
        
    @classmethod
    def SetEditorGeometry( cls, geo ):
        geo.setPythonTag( TAG_IGNORE, True )
        geo.setLightOff()
        geo.node().adjustDrawMask( *base.GetEditorRenderMasks() )
        cls.geo = geo
        
    def SetupNodePath( self, np ):
        GameNodePath.SetupNodePath( self, np )
        
        if self.geo is not None:
            self.geo.copyTo( np )
            
        if self.pickable:
            np.setPythonTag( TAG_PICKABLE, self.pickable )
            
    def OnSelect( self, np ):
        """Add a bounding box to the indicated node."""
        bbox = DirectBoundingBox( np, (1, 1, 1, 1) )
        bbox.show()
        bbox.lines.setPythonTag( TAG_IGNORE, True )
        bbox.lines.node().adjustDrawMask( *base.GetEditorRenderMasks() )
        np.setPythonTag( TAG_BBOX, bbox )
        return bbox
    
    def OnDeselect( self, np ):
        """Remove the bounding box from the indicated node."""
        bbox = np.getPythonTag( TAG_BBOX )
        if bbox is not None:
            bbox.lines.removeNode()
        np.clearPythonTag( TAG_BBOX )
    
    def OnDelete( self, np ):
        pass
    
    def GetTags( self ):
        tags = self.data.getPythonTag( TAG_PYTHON_TAGS )
        if tags is not None:
            return [tag for tag in tags if tag in base.game.nodeMgr.pyTagWrappers]
        
        return []
    
    def GetChildren( self ):
        children = []
        
        # Add wrappers for python objects.
        for tag in self.GetTags():
            pyObj = self.data.getPythonTag( tag )
            pyObjWrpr = base.game.nodeMgr.pyTagWrappers[tag]
            children.append( pyObjWrpr( pyObj ) )
        
        # Add wrappers for child NodePaths.
        for np in self.data.getChildren():
            if not np.getPythonTag( TAG_IGNORE ):
                children.append( base.game.nodeMgr.Wrap( np ) )
            
        return children
        
    def GetId( self ):
        return self.data.getTag( TAG_NODE_UUID )
    
    def SetId( self, id ):
        self.data.setTag( TAG_NODE_UUID, id )
    
    def GetParent( self ):
        return self.data.getParent()
    
    def GetName( self ):
        return self.data.getName()
    
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
        return not self.data.getPythonTag( TAG_DO_NOT_SAVE )