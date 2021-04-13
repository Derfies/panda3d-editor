from pandaEditor.nodes.base import Base


class SceneRoot(Base):
    
    def GetChildren(self):
        children = []
        comps = (render2d, render) + tuple(base.scene.comps.keys())
        for comp in comps:
            children.append(base.node_manager.Wrap(comp))
        return children
