import math

from panda3d.core import Mat4, Vec3, Point3, Plane, NodePath
from panda3d.core import CollisionSphere, CollisionPolygon
from panda3d.core import BillboardEffect

from p3d import commonUtils
from p3d.geometry import Arc, Line
from .axis import Axis
from .base import Base
from .constants import *


class Rotation(Base):
    
    def __init__(self, *args, **kwargs):
        Base.__init__(self, *args, **kwargs)
        
        # Create the 'ball' border
        self.border = self.CreateCircle(GREY, 1)
        
        # Create the collision sphere - except for the camera normal, all axes
        # will use this single collision object
        self.collSphere = CollisionSphere(0, 1)
        
        # Create x, y, z and camera normal axes
        self.axes.append(self.CreateRing(Vec3(1, 0, 0), RED, 
                                           Vec3(0, 0, 90)))
        self.axes.append(self.CreateRing(Vec3(0, 1, 0), GREEN, 
                                           Vec3(0, 90, 0)))
        self.axes.append(self.CreateRing(Vec3(0, 0, 1), BLUE, 
                                           Vec3(0, 0, 0)))
        
        # DEBUG
        self.foobar = self.CreateCamCircle(TEAL, 1.2)
        self.axes.append(self.foobar)
    
    def CreateRing(self, vector, colour, rot):
        
        # Create an arc
        arc = Arc(numSegs=32, degrees=180, axis=Vec3(0, 0, 1))
        arc.setH(180)
        
        # Create the axis from the arc
        axis = Axis(self.name, vector, colour)
        axis.AddGeometry(arc, sizeStyle=SCALE)
        axis.AddCollisionSolid(self.collSphere, sizeStyle=SCALE)
        axis.reparentTo(self)
        
        # Create the billboard effect and apply it to the arc. We need an
        # extra NodePath to help the billboard effect so it orients properly.
        hlpr = NodePath('helper')
        hlpr.setHpr(rot)
        hlpr.reparentTo(self)
        arc.reparentTo(hlpr)
        bbe = BillboardEffect.make(Vec3(0, 0, 1), False, True, 0, 
                                    self.camera, (0, 0, 0))
        arc.setEffect(bbe)
        
        return axis
    
    def CreateCircle(self, colour, radius):
        
        # Create a circle
        arc = Arc(radius, numSegs=64, axis=Vec3(0, 1, 0))
        arc.setColorScale(colour)
        arc.setLightOff()
        arc.reparentTo(self)
        
        # Set the billboard effect
        arc.setBillboardPointEye()
        
        return arc
    
    def CreateCamCircle(self, colour, radius):
        
        # Create the geometry and collision
        circle = self.CreateCircle(colour, radius)
        collPoly = CollisionPolygon(Point3(-1.2, 0, -1.2), Point3(-1.25, 0, 1.25), Point3(1.25, 0, 1.25), Point3(1.25, 0, -1.25))
        
        # Create the axis, add the geometry and collision
        self.camAxis = Axis(self.name, CAMERA_VECTOR, colour, planar=True, default=True)
        self.camAxis.AddGeometry(circle,  sizeStyle=SCALE)
        self.camAxis.AddCollisionSolid(collPoly, sizeStyle=SCALE)
        self.camAxis.reparentTo(self)
        
        return self.camAxis
        
    def SetSize(self, factor):
        Base.SetSize(self, factor)
        
        # Scale up any additional geo
        self.border.setScale(self.size)
    
    def GetAxis(self, collEntry):
        axis = Base.GetAxis(self, collEntry)
        
        # Return None if the axis is None
        if axis is None:
            return None
        
        if axis.vector != CAMERA_VECTOR:
            
            # Return the axis from the specified normal within a tolerance of 
            # degrees
            normal = collEntry.getSurfaceNormal(self)
            normal.normalize()
            for axis in self.axes:
                if math.fabs(normal.angleDeg(axis.vector) - 90) < (2.5 / self.size):
                    return axis
        else:
            
            # Get the collision point on the poly, return the axis if the
            # mouse is within tolerance of the circle
            point = collEntry.getSurfacePoint(collEntry.getIntoNodePath())
            length = Vec3(point / 1.25).length()
            if length > 0.9 and length < 1:
                return axis
        
    def Update(self, task):
        Base.Update(self, task)
        
        # DEBUG - make the camera normal collision plane look at the camera.
        # Probably should be a better way to do this.
        self.camAxis.collNodePaths[0].lookAt(self.camera)
        
        return task.cont
        
    def Transform(self):
        
        startVec = self.startVec
        
        axis = self.GetSelectedAxis()
        if axis is not None and axis.vector == CAMERA_VECTOR:
            endVec = self.getRelativeVector(self.rootNp, self.GetAxisPoint(axis) - self.getPos())
            
            cross = startVec.cross(endVec)
            direction = self.getRelativeVector(self.camera, Vec3(0, -1, 0)).dot(cross)
            sign = math.copysign(1, direction)
            
            # Get the rotation axis
            rotAxis = self.getRelativeVector(self.camera, Vec3(0, -1, 0)) * sign
        else:
            if self.collEntry.getIntoNode() == self.initCollEntry.getIntoNode():
                endVec = self.collEntry.getSurfaceNormal(self)
            else:
                endVec = self.getRelativeVector(self.rootNp, self.GetAxisPoint(self.foobar) - self.getPos())
            
            # If an axis is selected then constrain the vectors by projecting
            # them onto a plane whose normal is the axis vector
            if axis is not None:
                plane = Plane(axis.vector, Point3(0))
                startVec = Vec3(plane.project(Point3(startVec)))
                endVec = Vec3(plane.project(Point3(endVec) ))
            
            # Get the rotation axis
            rotAxis = endVec.cross(startVec) * -1
            
        # Return if the rotation vector is not valid, ie it does not have any
        # length
        if not rotAxis.length():
            return
        
        # Normalize all vectors
        startVec.normalize()
        endVec.normalize()
        rotAxis.normalize()

        # Get the amount of degrees to rotate
        degs = startVec.angleDeg(endVec)
        
        # Transform the gizmo if in local rotation mode
        newRotMat = Mat4().rotateMat(degs, rotAxis)
        if self.local:
            self.setMat(newRotMat * self.getMat())
            
        # Transform all attached node paths
        for i, np in enumerate(self.attachedNps):
            
            # Split the transform into scale, rotation and translation
            # matrices
            transMat, rotMat, scaleMat = commonUtils.GetTrsMatrices(np.getTransform())
            
            # Perform transforms in local or world space
            if self.local:
                np.setMat(scaleMat * newRotMat * rotMat * transMat)
            else:
                self.initNpXforms[i].getQuat().extractToMatrix(rotMat)
                np.setMat(scaleMat * rotMat * newRotMat * transMat)
                    
    def OnNodeMouse1Down(self, planar, collEntry):
        Base.OnNodeMouse1Down(self, planar, collEntry)
        
        # Store the initial collision entry
        self.initCollEntry = collEntry
        
        # If the selected axis is the camera vector then use a point on the
        # plane whose normal is the camera vector as the starting vector,
        # otherwise use the surface normal from the collision with the sphere
        axis = self.GetSelectedAxis()
        if axis is not None and axis.vector == CAMERA_VECTOR:
            self.startVec = self.getRelativeVector(self.rootNp, self.startAxisPoint - self.getPos())
        else:
            self.startVec = self.initCollEntry.getSurfaceNormal(self)
        
    def OnMouse2Down(self):
        Base.OnMouse2Down(self)
        
        axis = self.GetSelectedAxis()
        if (hasattr(self, 'collEntry') and hasattr(self, 'initCollEntry') and 
             self.collEntry.getIntoNode() != self.initCollEntry.getIntoNode()):
            self.startVec = self.getRelativeVector(self.rootNp, self.GetAxisPoint(self.foobar) - self.getPos())
        else:
            self.startVec = self.getRelativeVector(self.rootNp, self.startAxisPoint - self.getPos())

        # TODO:
        # AttributeError: 'Rotation' object has no attribute 'startAxisPoint'
    
    def OnNodeMouseOver(self, collEntry):
        Base.OnNodeMouseOver(self, collEntry)
        
        # Store the collision entry
        self.collEntry = collEntry