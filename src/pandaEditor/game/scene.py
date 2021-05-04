from p3d.object import Object


class Scene(Object):

    cType = 'SceneRoot'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.objects = {}
        self.physics_world = None
        self.physics_task = None
    
    def register_component(self, comp):
        self.objects[comp.data] = comp._metaobject
        del comp._metaobject

    def deregister_component(self, comp):
        del self.objects[comp.data]
