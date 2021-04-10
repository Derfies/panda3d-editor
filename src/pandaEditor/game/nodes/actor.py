import panda3d.core as pm
from direct.actor.Actor import Actor as P3dActor

import p3d
from .constants import *
from .modelRoot import ModelRoot
from .attributes import Attribute as Attr, PyTagAttribute as PTAttr


class Actor( ModelRoot ):
    
    def __init__( self, *args, **kwargs ):
        ModelRoot.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            PTAttr( 'Anims', dict, self.GetAnimDict, self.SetAnimDict, pyTagName=TAG_ACTOR ),
            parent='Actor'
        )
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        wrpr = super( Actor, cls ).Create( *args, **kwargs )
        
        actor = P3dActor( wrpr.data )
        actor.setTag( TAG_NODE_TYPE, 'Actor' )
        actor.setTag( TAG_NODE_UUID, wrpr.data.getTag( TAG_NODE_UUID ) )
        actor.setPythonTag( TAG_MODEL_PATH, str( wrpr.data.node().getFullpath() ) )
        actor.setPythonTag( TAG_ACTOR, actor )
        
        return cls( actor.getGeomNode() )
    
    def Duplicate( self ):
        dupeNp = ModelRoot.Duplicate( self )
        
        actor = P3dActor( dupeNp )
        actor.setTag( TAG_NODE_TYPE, 'Actor' )
        actor.setPythonTag( TAG_ACTOR, actor )
        actor.reparentTo( self.data.getParent() )
        actor.setTransform( dupeNp.getTransform() )
        actor.setName( dupeNp.getName() )
                         
        dupeNp.detachNode()
        
        # Copy animations over to the new actor.
        oldAnims = self.GetAnimDict( self.data.getPythonTag( TAG_ACTOR ) )
        self.SetAnimDict( actor, oldAnims )
        
        return actor.getGeomNode()
    
    def GetAnimDict( self, actor ):
        animDict = {}
        for name in P3dActor.getAnimNames( actor ):
            filePath = actor.getAnimFilename( name )
            animDict[name] = base.project.GetRelModelPath( filePath )
            
        return animDict
        
    def SetAnimDict( self, actor, animDict ):
        actor.removeAnimControlDict()
        
        myDict = {}
        for key, value in animDict.items():
            try:
                pandaPath = pm.Filename.fromOsSpecific( value )
            except TypeError:
                pandaPath = value
            myDict[key] = pandaPath
            
        actor.loadAnims( myDict )