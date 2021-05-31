import panda3d.core as pc
from direct.showbase.PythonUtil import getBase as get_base
from panda3d.core import Vec2, Vec3

from p3d.camera import Camera, CAM_USE_DEFAULT, CAM_VIEWPORT_AXES
from p3d.mouse import Mouse, MOUSE_ALT


class EditorCamera(Mouse, Camera):
    
    """Base editor camera class."""
    
    def __init__(self, *args, **kwargs):
        self.orbit_sensitivity = kwargs.pop('orbit_sensitivity', 1)
        self.dolly_sensitivity = kwargs.pop('dolly_sensitivity', 1)
        self.zoom_sensitivity = kwargs.pop('zoom_sensitivity', 1)
        kwargs['pos'] = kwargs.pop('pos', (-250, -250, 200))
        kwargs['style'] = kwargs.pop(
            'style',
            CAM_USE_DEFAULT | CAM_VIEWPORT_AXES
        )
        super().__init__(*args, **kwargs)
        
        # Create mouse
        base.disableMouse()
        # self.mouse = Mouse('mouse', *args, **kwargs)
        # self.mouse.Start()
    
    def OnUpdate(self, task):
        """
        Task to control mouse events. Gets called every frame and will update
        the scene accordingly.

        """
        super().OnUpdate(task)
        
        # Return if no mouse is found or alt not down
        if not self.mouseWatcherNode.hasMouse() or not MOUSE_ALT in self.modifiers:
            return

        dx = self.dx
        dy = self.dy

        #print(globalClock.getDt())

        win_size = get_base().win.get_size()
        #rx, ry = 1600.0 / win_size.x, 900.0 / win_size.y
        # #print(rx, ry)

        # dy *= ry

        #print(task.dt)

        #dx *= task.dt * 1000.0
        #dy *= task.dt * 1000.0
        dx *= 0.1
        dy *= 0.1


        corrected_dx = dx * 1.0 / win_size.x * win_size.x
        corrected_dy = dy * 1.0 / win_size.y * win_size.y

        '''
        #get the real size of the viewport
        var root_size = $"/root".size
        
        #calculate black strip
        var correction = (OS.get_window_size() - root_size)/2.0
        
        #we use fixed resolution of 1600 * 900
        var ratio = Vector2(1600.0, 900.0)/root_size
        
        var real_mouse_position = (get_viewport().get_mouse_position()-correction)*ratio
        '''

        # Attempt to compensate for window size.
        # dx *= 1.0 / base.win.getXSize() * 500
        # dy *= 1.0 / base.win.getYSize() * 500

        # print('corrected_dx:', corrected_dx)
        
        # ORBIT - If left mouse down
        if self.buttons[0]:
            self.Orbit(Vec2(
                corrected_dx * self.orbit_sensitivity,
                corrected_dy * self.orbit_sensitivity,
            ))
        
        # DOLLY - If middle mouse down
        elif self.buttons[1]:
            self.Move(Vec3(
                corrected_dx * self.dolly_sensitivity,
                0,
                -corrected_dy * self.dolly_sensitivity,
            ))
            
        # ZOOM - If right mouse down
        elif self.buttons[2]:
            self.Move(Vec3(
                0,
                -corrected_dx * self.zoom_sensitivity,
                0,
            ))
