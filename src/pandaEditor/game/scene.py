import uuid

from direct.showbase.PythonUtil import getBase as get_base

from p3d.object import Object


class Scene(Object):

    cType = 'SceneRoot'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.comps = {}
        get_base().scene = self
        self.physics_world = None
        self.physics_task = None
    
    def register_component(self, comp):
        id = str(uuid.uuid4())
        self.comps[comp] = id
        
    def deregister_component(self, comp):
        if comp in self.comps:
            del self.comps[comp]
            
    def get_physics_world(self, foo):
        return self.physics_world

    def set_physics_world(self, cookie, phWorld):
        self.physics_world = phWorld
    
    def clear_physics_world(self, cookie):
        self.physics_world = None
