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
        
        self.AddAttributes(
            PTAttr( 'Anim Names', dict, self.GetAnimDict, self.SetAnimDict, pyTagName=TAG_ACTOR ),
            parent='Actor'
        )
        
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
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        wrpr = super( Actor, cls ).Create( *args, **kwargs )
        
        actor = P3dActor( wrpr.data )
        actor.setTag( TAG_NODE_TYPE, 'Actor' )
        actor.setPythonTag( 'modelPath', str( wrpr.data.node().getFullpath() ) )
        actor.setTag( TAG_NODE_UUID, wrpr.data.getTag( TAG_NODE_UUID ) )
        actor.getGeomNode().setPythonTag( TAG_ACTOR, actor )
        
        return cls( actor.getGeomNode() )