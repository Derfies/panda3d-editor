from panda3d.core import Point3, NodePath, GeomEnums
from panda3d.core import CollisionNode, CollisionTube

from .constants import *


class Axis( NodePath ):
        
    def __init__( self, name, vector, colour, planar=False, default=False ):
        NodePath.__init__( self, name )
        
        self.name = name
        self.vector = vector
        self.colour = colour
        self.planar = planar
        self.default = default
        
        self.highlited = False
        self.selected = False
        self.size = 1
        
        self.geoms = []
        self.collNodes = []
        self.collNodePaths = []
        
    def AddGeometry( self, geom, pos=Point3(0, 0, 0), colour=None, 
                     highlight=True, sizeStyle=TRANSLATE ):
        """
        Add geometry to represent the axis and move it into position. If the
        geometry is a line make sure to call setLightOff or else it won't
        look right.
        """
        geom.setPos( pos )
        geom.setPythonTag( 'highlight', highlight )
        geom.setPythonTag( 'sizeStyle', sizeStyle )
        geom.reparentTo( self )
        
        # If colour is not specified then use the axis colour
        if colour is None:
            colour = self.colour
        geom.setColorScale( colour )
        
        # Set light off if the geometry is a line
        if geom.node().getGeom( 0 ).getPrimitiveType() == GeomEnums.PTLines:
            geom.setLightOff()
        
        self.geoms.append( geom )
        
    def AddCollisionSolid( self, collSolid, pos=Point3(0, 0, 0), 
                           sizeStyle=TRANSLATE ):
        """Add a collision solid to the axis and move it into position."""
        # Create the collision node and add the solid
        collNode = CollisionNode( self.name )
        collNode.addSolid( collSolid )
        self.collNodes.append( collNode )
        
        # Create a node path and move it into position
        collNodePath = self.attachNewNode( collNode )
        collNodePath.setPos( pos )
        collNodePath.setPythonTag( 'sizeStyle', sizeStyle )
        self.collNodePaths.append( collNodePath )
        
    def SetSize( self, size ):
        """
        Change the size of the gizmo. This isn't just the same as scaling all
        the geometry and collision - sometimes this just means pushing the
        geometry along the axis instead.
        """
        oldSize = self.size
        self.size = size
        
        nodePaths = self.geoms + self.collNodePaths
        for nodePath in nodePaths:
            
            # Get the size style
            sizeStyle = nodePath.getPythonTag( 'sizeStyle' )
            if sizeStyle & NONE:
                continue
            
            # Set scale
            if sizeStyle & SCALE:
                nodePath.setScale( self.size )
                
            # Set position
            if sizeStyle & TRANSLATE:
                
                # Get the position of the node path relative to the axis end
                # point (vector), then move the geometry and reapply this
                # offset 
                diff = ( self.vector * oldSize ) - nodePath.getPos()
                nodePath.setPos( Point3( ( self.vector * self.size ) - diff ) )
                
            # Should only be used for collision tubes
            if sizeStyle & TRANSLATE_POINT_B:
                collSolid = nodePath.node().modifySolid( 0 )
                if type( collSolid ) == CollisionTube:
                    
                    # Get the position of the capsule's B point relative to
                    # the axis end point (vector), then move the point and
                    # reapply this offset 
                    diff = ( self.vector * oldSize ) - collSolid.getPointB()
                    collSolid.setPointB( Point3( ( self.vector * self.size ) - diff ) )
        
    def Select( self ):
        """
        Changed the colour of the axis to the highlight colour and flag as
        being selected.
        """
        self.selected = True
        self.Highlight()
        
    def Deselect( self ):
        """
        Reset the colour of the axis to the original colour and flag as being
        unselected.
        """
        self.selected = False
        self.Unhighlight()
        
    def Highlight( self ):
        """Highlight the axis by changing it's colour."""
        for geom in self.geoms:
            if geom.getPythonTag( 'highlight' ):
                geom.setColorScale( YELLOW )
        
    def Unhighlight( self ):
        """Remove the highlight by resetting to the axis colour."""
        for geom in self.geoms:
            if geom.getPythonTag( 'highlight' ):
                geom.setColorScale( self.colour )