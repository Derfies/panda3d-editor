from game.nodes.constants import TAG_MODEL_ROOT_CHILD


class ModelRoot:
    
    @classmethod
    def Create(cls, *args, **kwargs):
        wrpr = super(ModelRoot, cls).Create(*args, **kwargs)
        
        # Tag each descendant NodePath as a child of a model root. This edits
        # of these NodePaths to be saved out.
        for childNp in wrpr.data.findAllMatches('**/*'):
            childNp.setPythonTag(TAG_MODEL_ROOT_CHILD, True)
        
        return wrpr
    
    def GetFullPath(self, node):
        panda_path = super().GetFullPath(node)
        return base.project.GetRelModelPath(panda_path)
