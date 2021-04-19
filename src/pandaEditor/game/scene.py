import uuid

from p3d.object import Object


class Scene(Object):

    cType = 'SceneRoot'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.comps = {}
        self.physics_world = None
        self.physics_task = None
    
    def register_component(self, comp):
        self.comps[comp] = str(uuid.uuid4())
        
    def deregister_component(self, comp):
        del self.comps[comp]
            
    def get_physics_world(self):
        return self.physics_world

    def set_physics_world(self, physics_world):
        self.physics_world = physics_world
    
    def clear_physics_world(self):
        self.physics_world = None
