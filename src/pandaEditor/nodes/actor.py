from nodes.constants import TAG_PICKABLE
from game.nodes.constants import TAG_MODEL_PATH


class Actor:
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = super().Create(*args, **kwargs)
        wrpr.data.setPythonTag(TAG_PICKABLE, True)
        return wrpr
    
    def Duplicate(self):
        dupeNp = super().Duplicate()
        dupeNp.setPythonTag(TAG_PICKABLE, True)
        return dupeNp
    
    def GetFullPath(self, node):
        modelPath = node.getPythonTag(TAG_MODEL_PATH)
        relPath = base.project.GetRelModelPath(modelPath)
        return relPath
