import uuid

from p3d.object import Object


class Scene(Object):

    cType = 'SceneRoot'

    def __init__(self, *args, **kwargs):
        Object.__init__(self, *args, **kwargs)
        
        self.comps = {}
        base.scene = self
        self.physicsWorld = None
        self.physicsTask = None
    
    def RegisterComponent(self, comp):
        id = str(uuid.uuid4())
        self.comps[comp] = id
        
    def DeregisterComponent(self, comp):
        if comp in self.comps:
            del self.comps[comp]
            
    def GetPhysicsWorld(self, foo):
        return self.physicsWorld
    
    def SetPhysicsWorld(self, cookie, phWorld):
        self.physicsWorld = phWorld
    
    def ClearPhysicsWorld(self, cookie):
        self.physicsWorld = None
