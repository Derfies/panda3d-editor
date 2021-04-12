from nodes.constants import TAG_PICKABLE
from game.nodes.actor import Actor as GameActor
from game.nodes.constants import TAG_MODEL_PATH


class Actor(GameActor):
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = super(Actor, cls).Create(*args, **kwargs)
        wrpr.data.setPythonTag(TAG_PICKABLE, True)
        return wrpr
    
    def Duplicate(self):
        dupeNp = GameActor.Duplicate(self)
        dupeNp.setPythonTag(TAG_PICKABLE, True)
        return dupeNp
    
    def GetFullPath(self, node):
        modelPath = node.getPythonTag(TAG_MODEL_PATH)
        relPath = base.project.GetRelModelPath(modelPath)
        return relPath
