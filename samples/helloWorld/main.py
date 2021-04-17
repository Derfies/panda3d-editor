from math import pi, sin, cos

import panda3d.core as pc
from direct.task import Task
from direct.interval.IntervalGlobal import Sequence

from game.showbase import ShowBase
 
 
class MyApp(ShowBase):
    
    def __init__(self):
        super().__init__()
        
        # Load the level.
        self.load_scene('scenes/hello_world.xml')
 
        # Disable the camera trackball controls.
        self.disable_mouse()
 
        # Add the spinCameraTask procedure to the task manager.
        self.task_mgr.add(self.spin_camera_task, 'spin_camera_task')
        
        # Find the panda actor placed in the scene.
        panda_component = self.node_manager.wrap(self.render.find('panda_walk_character'))
        self.panda_actor = panda_component.GetActor()
        self.panda_actor.loop('walk')
 
        # Create the four lerp intervals needed for the panda to
        # walk back and forth.
        pandaPosInterval1 = self.panda_actor.posInterval(
            13,
            pc.Point3(0, -10, 0),
            startPos=pc.Point3(0, 10, 0)
        )
        pandaPosInterval2 = self.panda_actor.posInterval(
            13,
            pc.Point3(0, 10, 0),
            startPos=pc.Point3(0, -10, 0)
        )
        pandaHprInterval1 = self.panda_actor.hprInterval(
            3,
            pc.Point3(180, 0, 0),
            startHpr=pc.Point3(0, 0, 0)
        )
        pandaHprInterval2 = self.panda_actor.hprInterval(
            3,
            pc.Point3(0, 0, 0),
            startHpr=pc.Point3(180, 0, 0)
        )
 
        # Create and play the sequence that coordinates the intervals.
        self.panda_pace = Sequence(
            pandaPosInterval1,
            pandaHprInterval1,
            pandaPosInterval2,
            pandaHprInterval2,
            name='panda_pace'
        )
        self.panda_pace.loop()
 
    # Define a procedure to move the camera.
    def spin_camera_task(self, task):
        degrees = task.time * 6.0
        radians = degrees * (pi / 180.0)
        self.camera.setPos(20 * sin(radians), -20.0 * cos(radians), 3)
        self.camera.setHpr(degrees, 0, 0)
        return Task.cont
 
 
app = MyApp()
app.run()