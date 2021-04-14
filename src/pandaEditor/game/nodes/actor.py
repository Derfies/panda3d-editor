import panda3d.core as pm
from direct.actor.Actor import Actor as P3dActor

from game.nodes.attributes import PyTagAttribute
from game.nodes.constants import (
    TAG_ACTOR, TAG_MODEL_PATH, TAG_NODE_TYPE, TAG_NODE_UUID
)
from game.nodes.modelroot import ModelRoot


class Actor(ModelRoot):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.AddAttributes(
            PyTagAttribute(
                'Anims',
                dict,
                self.GetAnimDict,
                self.SetAnimDict,
                pyTagName=TAG_ACTOR
            ),
            parent='Actor'
       )
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = super(Actor, cls).Create(*args, **kwargs)
        
        actor = P3dActor(wrpr.data)
        actor.setTag(TAG_NODE_TYPE, 'Actor')
        actor.setTag(TAG_NODE_UUID, wrpr.data.getTag(TAG_NODE_UUID))
        actor.setPythonTag(TAG_MODEL_PATH, str(wrpr.data.node().getFullpath()))
        actor.setPythonTag(TAG_ACTOR, actor)
        
        return cls(actor.getGeomNode())
    
    def Duplicate(self):
        dupeNp = ModelRoot.Duplicate(self)
        
        actor = P3dActor(dupeNp)
        actor.setTag(TAG_NODE_TYPE, 'Actor')
        actor.setPythonTag(TAG_ACTOR, actor)
        actor.reparentTo(self.data.getParent())
        actor.setTransform(dupeNp.getTransform())
        actor.setName(dupeNp.getName())
                         
        dupeNp.detachNode()
        
        # Copy animations over to the new actor.
        oldAnims = self.GetAnimDict(self.data.getPythonTag(TAG_ACTOR))
        self.SetAnimDict(actor, oldAnims)
        
        return actor.getGeomNode()
    
    def GetAnimDict(self, actor):
        animDict = {}
        for name in P3dActor.getAnimNames(actor):
            filePath = actor.getAnimFilename(name)
            animDict[name] = base.project.GetRelModelPath(filePath)
            
        return animDict
        
    def SetAnimDict(self, actor, animDict):
        actor.removeAnimControlDict()
        
        myDict = {}
        for key, value in animDict.items():
            try:
                pandaPath = pm.Filename.fromOsSpecific(value)
            except TypeError:
                pandaPath = value
            myDict[key] = pandaPath
            
        actor.loadAnims(myDict)
