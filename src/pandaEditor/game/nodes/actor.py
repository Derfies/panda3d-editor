import pandac.PandaModules as pm
from direct.actor.Actor import Actor as P3dActor

import p3d
from constants import *
from modelRoot import ModelRoot
from attributes import Attribute as Attr, PyTagAttribute as PTAttr


TAG_ACTOR = 'p3d_actor'


class Actor( ModelRoot ):
    
    def __init__( self, *args, **kwargs ):
        ModelRoot.__init__( self, *args, **kwargs )
        
        pAttr = Attr( 'Actor' )
        pAttr.children.extend( 
            [
                PTAttr( 'Anim Names', dict, self.GetAnimDict, self.SetAnimDict, pyTagName=TAG_ACTOR )
            ]
        )
        self.attributes.append( pAttr )
        
    def GetAnimDict( self, actor ):
        animDict = {}
        for name in P3dActor.getAnimNames( actor ):
            animDict[name] = actor.getAnimFilename( name ) 
            
        return animDict
        
    def SetAnimDict( self, actor, animDict ):
        myDict = {}
        for key, value in animDict.items():
            try:
                pandaPath = pm.Filename.fromOsSpecific( value )
            except TypeError:
                pandaPath = value
            myDict[key] = pandaPath
            
        actor.loadAnims( myDict )
        
    def GetCreateArgs( self ):
        return {'modelPath':self.GetRelModelPath()}
        
    def Create( self, *args, **kwargs ):
        np = ModelRoot.Create( self, *args, **kwargs )
        
        actor = P3dActor( np )
        actor.setTag( 'type', 'Actor' )
        actor.setPythonTag( 'modelPath', str( np.node().getFullpath() ) )
        actor.setTag( TAG_NODE_UUID, np.getTag( TAG_NODE_UUID ) )
        self.data = actor.getGeomNode()
        actor.getGeomNode().setPythonTag( TAG_ACTOR, actor )
        
        return actor