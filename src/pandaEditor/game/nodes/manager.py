from constants import *


class Manager( object ):
    
    def __init__( self ):
        from nodePath import NodePath
        from render import Render
        from actor import Actor
        from pandaNode import PandaNode
        from collisionNode import CollisionNode
        from camera import Camera
        from baseCam import BaseCam
        from modelNode import ModelNode
        from baseCamera import BaseCamera
        from modelRoot import ModelRoot

        from light import Light
        from ambientLight import AmbientLight
        from pointLight import PointLight
        from directionalLight import DirectionalLight
        from spotlight import Spotlight
        
        self.nodeWrappers = {
            'NodePath':NodePath,
            'Render':Render,
            'PandaNode':PandaNode,
            'Actor':Actor,
            'CollisionNode':CollisionNode,
            'Camera':Camera,
            'BaseCam':BaseCam,
            'ModelNode':ModelNode,
            'BaseCamera':BaseCamera,
            'ModelRoot':ModelRoot,
            
            'Light':Light,
            'AmbientLight':AmbientLight,
            'PointLight':PointLight,
            'DirectionalLight':DirectionalLight,
            'Spotlight':Spotlight
        }
        
        self.pyTagWrappers = {}
        
    def Create( self, nTypeStr, *args ):
        Wrpr = self.nodeWrappers[nTypeStr]
        wrpr = Wrpr()
        return wrpr.Create( *args )
    
    def Wrap( self, np ):
        Wrpr = self.GetWrapper( np )
        if Wrpr is not None:
            return Wrpr( np )
        
        return None
        
    def GetWrapper( self, np ):
        typeStr = self.GetTypeString( np )
        if typeStr in self.nodeWrappers:
            return self.nodeWrappers[typeStr]
        
        return None
    
    def GetWrapperByName( self, nTypeStr ):
        if nTypeStr in self.nodeWrappers:
            return self.nodeWrappers[nTypeStr]
        
        return None
        
    def GetTypeString( self, np ):
        """Return the type of the NodePath."""
        nType = np.node().getTag( TAG_NODE_TYPE )
        if not nType:
            nType = type( np.node() ).__name__
        
        return nType