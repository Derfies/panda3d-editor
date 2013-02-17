from game.nodes.sceneRoot import SceneRoot as GameSceneRoot


class SceneRoot( GameSceneRoot ):
    
    def GetChildren( self ):
        children = []
        
        comps = [render] + base.scene.comps.keys()
        for comp in comps:
            children.append( base.game.nodeMgr.Wrap( comp ) )
        
        return children