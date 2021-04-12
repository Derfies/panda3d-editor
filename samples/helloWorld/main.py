from math import pi, sin, cos
 
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

import game
 
 
class MyApp(ShowBase):
    
    def __init__(self):
        super().__init__()
        
        # Create the game base and load the level.
        self.game = game.Base()
        self.Load('scenes/helloWorld.xml')
 
        # Disable the camera trackball controls.
        self.disableMouse()
 
        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, 'SpinCameraTask')
        
        # Find the panda actor placed in the scene.
        pandaWrpr = base.node_manager.Wrap(render.find('panda_walk_character'))
        self.pandaActor = pandaWrpr.GetActor()
        self.pandaActor.loop('walk')
 
        # Create the four lerp intervals needed for the panda to
        # walk back and forth.
        pandaPosInterval1 = self.pandaActor.posInterval(13,
                                                         Point3(0, -10, 0),
                                                         startPos=Point3(0, 10, 0))
        pandaPosInterval2 = self.pandaActor.posInterval(13,
                                                         Point3(0, 10, 0),
                                                         startPos=Point3(0, -10, 0))
        pandaHprInterval1 = self.pandaActor.hprInterval(3,
                                                         Point3(180, 0, 0),
                                                         startHpr=Point3(0, 0, 0))
        pandaHprInterval2 = self.pandaActor.hprInterval(3,
                                                         Point3(0, 0, 0),
                                                         startHpr=Point3(180, 0, 0))
 
        # Create and play the sequence that coordinates the intervals.
        self.pandaPace = Sequence(pandaPosInterval1,
                                   pandaHprInterval1,
                                   pandaPosInterval2,
                                   pandaHprInterval2,
                                   name='pandaPace')
        self.pandaPace.loop()
 
    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont
 
 
app = MyApp()
app.run()