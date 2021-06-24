import panda3d.core as pm
from direct.directtools.DirectUtil import ROUND_TO

from p3d import commonUtils as utils
from p3d.geometry import cone, Square, Line
from .axis import Axis
from .base import Base
from .constants import *


TOL = 0.1


class Translation(Base):
    
    def __init__(self, *args, **kwargs):
        Base.__init__(self, *args, **kwargs)
        
        self._snp = False
        self._snpAmt = 0.5
        
        # Create x, y, z and camera normal axes
        self.axes.append(self.CreateArrow(pm.Vec3(1, 0, 0), RED))
        self.axes.append(self.CreateArrow(pm.Vec3(0, 1, 0), GREEN))
        self.axes.append(self.CreateArrow(pm.Vec3(0, 0, 1), BLUE))
        #self.axes.append(self.CreateArrow(pm.Vec3(1, 1, 0), YELLOW))
        #self.axes.append(self.CreateArrow(pm.Vec3(-2, 1, 0), TEAL))
        self.axes.append(self.CreateSquare(pm.Vec3(0, 0, 0), TEAL))
        
    def CreateArrow(self, vec, colour):
        
        # Create the geometry and collision
        vec.normalize()
        line = pm.NodePath(Line((0, 0, 0), vec))
        head = pm.NodePath(cone(0.05, 0.25, axis=vec, origin=vec * 0.125))
        collTube = pm.CollisionCapsule((0,0,0), pm.Point3(vec) * 0.95, 0.05)
        
        # Create the axis, add the geometry and collision
        axis = Axis(self.name, vec, colour)
        axis.AddGeometry(line, sizeStyle=SCALE)
        axis.AddGeometry(head, vec, colour)
        axis.AddCollisionSolid(collTube, sizeStyle=TRANSLATE_POINT_B)
        axis.reparentTo(self)
        
        return axis
    
    def CreateSquare(self, vec, colour):
        
        # Create the geometry and collision
        self.square = pm.NodePath(Square(0.2, 0.2, pm.Vec3(0, 1, 0)))
        self.square.setBillboardPointEye()
        collSphere = pm.CollisionSphere(0, 0.125)
        
        # Create the axis, add the geometry and collision
        axis = Axis(self.name, CAMERA_VECTOR, colour, planar=True, default=True)
        axis.AddGeometry(self.square, sizeStyle=NONE)
        axis.AddCollisionSolid(collSphere, sizeStyle=NONE)
        axis.reparentTo(self)
        
        return axis
    
    def _Snap(self, vec):
        if vec.length():
            snpLen = ROUND_TO(vec.length(), self._snpAmt)
            snapVec = vec / vec.length() * snpLen
            return snapVec
        else:
            return pm.Vec3(0)
    
    def Transform(self):
        axis = self.GetSelectedAxis()
        axisPoint = self.GetAxisPoint(axis)
        
        # Calculate delta and snapping.
        d = axisPoint - self.lastAxisPoint
        lastSnap = self._Snap(self._s)
        self._s += d
        thisSnap = self._Snap(self._s)
        
        if self._snp:
            
            # If snapping in planar mode or using the camera axis, snap to a
            # point on the ground plane.
            if axis.vector == CAMERA_VECTOR or self.planar:
                pnt = self.GetMousePlaneCollisionPoint(pm.Point3(0), 
                                                        pm.Vec3(0, 0, 1))
                pnt = utils.SnapPoint(pnt, self._snpAmt)
                
                self.setPos(render, pnt)
                for np in self.attachedNps:
                    np.setPos(render, pnt)
                    
                return
                
            # If snapping in world space, construct a plane where the mouse
            # clicked the axis and move all NodePaths so they intersect it.
            elif not self.local:
                pnt = utils.SnapPoint(self.startAxisPoint + d, self._snpAmt)
                pl = pm.Plane(axis.vector, pm.Point3(pnt))
                
                self.setPos(render, pl.project(self.getPos(render)))
                for np in self.attachedNps:
                    np.setPos(render, pl.project(np.getPos(render)))
                    
                return
            
            # Gone over the snap threshold - set the delta to the snap amount.
            elif thisSnap.compareTo(lastSnap, TOL):
                d.normalize()
                d *= self._snpAmt
                
                # BUG - need to resize to compensate for cam dist?
                
            # In snapping mode but haven't gone past the snap threshold.
            else:
                d = pm.Vec3(0)
            
        d = self.getRelativeVector(self.rootNp, d)
        self.setMat(pm.Mat4().translateMat(d) * self.getMat())
        
        # Adjust the size of delta by the gizmo size to get real world units.
        d = utils.ScalePoint(d, self.getScale())
        
        # Hack for fixing camera vector xforming in local mode.
        if self.local and axis.vector == CAMERA_VECTOR:
            d = self.rootNp.getRelativeVector(self, d)
            d = utils.ScalePoint(d, self.getScale(), True)
        
        # Xform attached NodePaths.
        for np in (self.attachedNps):
            if self.local and axis.vector != CAMERA_VECTOR:
                sclD = utils.ScalePoint(d, np.getScale(self.rootNp), True)
                np.setMat(pm.Mat4().translateMat(sclD) * np.getMat())
            else:
                np.setMat(self.rootNp, np.getMat(self.rootNp) * 
                           pm.Mat4().translateMat(d))
        
        self.lastAxisPoint = axisPoint
        
    def OnNodeMouse1Down(self, planar, collEntry):
        Base.OnNodeMouse1Down(self, planar, collEntry)
        
        self._s = pm.Vec3(0)
        
        # If in planar mode, clear the billboard effect on the center square
        # and make it face the selected axis
        axis = self.GetSelectedAxis()
        if self.planar and not axis.planar:
            self.square.clearBillboard()
            self.square.lookAt(self, pm.Point3(axis.vector))
        else:
            self.square.setHpr(pm.Vec3(0, 0, 0))
            self.square.setBillboardPointEye()
            
    def OnMouse2Down(self):
        Base.OnMouse2Down(self)
        
        self._s = pm.Vec3(0)
        
    def AcceptEvents(self):
        Base.AcceptEvents(self)
        
        self.accept('x', self.SetSnap, [True])
        self.accept('x-up', self.SetSnap, [False])
        
    def SetSnap(self, val):
        self._snp = val