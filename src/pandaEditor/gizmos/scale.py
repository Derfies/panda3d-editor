import math

from pandac.PandaModules import Mat4, Vec3, Point3, CollisionSphere, NodePath

from p3d import commonUtils
from p3d.geometry import Line, Box
from axis import Axis
from base import Base
from constants import *


class Scale( Base ):
    
    def __init__( self, *args, **kwargs ):
        Base.__init__( self, *args, **kwargs )
        
        self.complementary = False
        
        # Create x, y, z and center axes
        self.axes.append( self.CreateBox( Vec3(1, 0, 0), RED ) )
        self.axes.append( self.CreateBox( Vec3(0, 1, 0), GREEN ) )
        self.axes.append( self.CreateBox( Vec3(0, 0, 1), BLUE ) )
        self.axes.append( self.CreateCenter( Vec3(1, 1, 1), TEAL ) )
            
    def CreateBox( self, vector, colour ):
        
        # Create the geometry and collision
        line = NodePath( Line( (0, 0, 0), vector ) )
        box = Box( 0.1, 0.1, 0.1, origin=Point3(0.05, 0.05, 0.05) + vector * 0.05 )
        collSphere = CollisionSphere( Point3( vector * -0.05 ), 0.1 )
        
        # Create the axis, add the geometry and collision
        axis = Axis( self.name, vector, colour )
        axis.AddGeometry( line, colour=GREY, highlight=False, sizeStyle=SCALE )
        axis.AddGeometry( box, vector, colour )
        axis.AddCollisionSolid( collSphere, vector )
        axis.reparentTo( self )
        
        return axis
    
    def CreateCenter( self, vector, colour ):
        
        # Create the axis, add the geometry and collision
        axis = Axis( self.name, vector, colour, default=True )
        axis.AddGeometry( Box( 0.1, 0.1, 0.1, origin=Point3(0.05, 0.05, 0.05) ), sizeStyle=NONE )
        axis.AddCollisionSolid( CollisionSphere( 0, 0.1 ), sizeStyle=NONE )
        axis.reparentTo( self )
        
        return axis
    
    def Transform( self ):
        
        # Get the distance the mouse has moved during the drag operation -
        # compensate for how big the gizmo is on the screen
        axis = self.GetSelectedAxis()
        axisPoint = self.GetAxisPoint( axis )
        distance = ( axisPoint - self.initMousePoint ).length() / self.getScale()[0]
        
        # Using length() will give us a positive number, which doesn't work if
        # we're trying to scale down the object. Get the sign for the distance
        # from the dot of the axis and the mouse direction
        mousePoint = self.getRelativePoint( render, axisPoint ) - self.getRelativePoint( render, self.initMousePoint )
        direction = axis.vector.dot( mousePoint )
        sign = math.copysign( 1, direction )
        distance = distance * sign
        
        # Transform the gizmo
        if axis.vector == Vec3(1, 1, 1):
            for otherAxis in self.axes:
                otherAxis.SetSize( distance + self.size )
        else:
            axis.SetSize( distance + self.size )
            
        # Use the "complementary" vector if in complementary mode
        vector = axis.vector
        if self.complementary:
            vector = Vec3(1, 1, 1) - axis.vector
                    
        # Create a scale matrix from the resulting vector
        scaleVec = vector * ( distance + 1 ) + Vec3(1, 1, 1) - vector
        newScaleMat = Mat4().scaleMat( scaleVec )
        
        # Transform attached node paths
        for i, np in enumerate( self.attachedNps ):
            
            # Perform transforms in local or world space
            if self.local:
                np.setMat( newScaleMat * self.initNpXforms[i].getMat() )
            else:
                transMat, rotMat, scaleMat = commonUtils.GetTrsMatrices( self.initNpXforms[i] )
                np.setMat( scaleMat * rotMat * newScaleMat * transMat )
                
    def OnNodeMouse1Down( self, planar, collEntry ):
        
        # Cheating a bit here. We just need the planar flag taken from the
        # user ctrl-clicking the gizmo, none of the maths that come with it.
        # We'll use the complementary during the transform operation.
        self.complementary = planar
        planar = False
        
        Base.OnNodeMouse1Down( self, planar, collEntry )