from math import pi, sin, cos

import p3d


class CameraSpin(p3d.PandaBehaviour):
        
    def OnUpdate(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.np.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.np.setHpr(angleDegrees, 0, 0)