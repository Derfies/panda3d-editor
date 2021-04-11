from game.nodes.sceneRoot import SceneRoot as GameSceneRoot


class SceneRoot(GameSceneRoot):
    
    def GetChildren(self):
        children = []
        comps = (render2d, render) + tuple(base.scene.comps.keys())
        for comp in comps:
            children.append(base.game.node_manager.Wrap(comp))
        return children
