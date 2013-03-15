from constants import *


class Manager( object ):
    
    def __init__( self ):
        from base import Base
        from sceneRoot import SceneRoot
        
        from nodePath import NodePath
        from render import Render
        from actor import Actor
        from pandaNode import PandaNode
        from camera import Camera
        from baseCam import BaseCam
        from modelNode import ModelNode
        from baseCamera import BaseCamera
        from modelRoot import ModelRoot
        
        from collisionNode import CollisionNode
        from collisionSolids import CollisionBox
        from collisionSolids import CollisionRay
        from collisionSolids import CollisionSphere
        from collisionSolids import CollisionInvSphere
        from collisionSolids import CollisionTube

        from light import Light
        from ambientLight import AmbientLight
        from pointLight import PointLight
        from directionalLight import DirectionalLight
        from spotlight import Spotlight
        
        from texture import Texture
        from textureStage import TextureStage
        
        from bulletWorld import BulletWorld
        from bulletDebugNode import BulletDebugNode
        from bulletRigidBodyNode import BulletRigidBodyNode
        from bulletCharacterControllerNode import BulletCharacterControllerNode
        from bulletBoxShape import BulletBoxShape
        from bulletPlaneShape import BulletPlaneShape
        from bulletCapsuleShape import BulletCapsuleShape
        
        self.nodeWrappers = {
            'Base':Base,
            'SceneRoot':SceneRoot,
            
            'NodePath':NodePath,
            'PandaNode':PandaNode,
            'Render':Render,
            'Camera':Camera,
            'BaseCam':BaseCam,
            'ModelNode':ModelNode,
            'BaseCamera':BaseCamera,
            'ModelRoot':ModelRoot,
            'Actor':Actor,
            
            'CollisionNode':CollisionNode,
            'CollisionBox':CollisionBox,
            'CollisionRay':CollisionRay,
            'CollisionSphere':CollisionSphere,
            'CollisionInvSphere':CollisionInvSphere,
            'CollisionTube':CollisionTube,
            
            'Light':Light,
            'AmbientLight':AmbientLight,
            'PointLight':PointLight,
            'DirectionalLight':DirectionalLight,
            'Spotlight':Spotlight,
            
            'Texture':Texture,
            'TextureStage':TextureStage,
            
            'BulletWorld':BulletWorld,
            'BulletDebugNode':BulletDebugNode,
            'BulletRigidBodyNode':BulletRigidBodyNode,
            'BulletCharacterControllerNode':BulletCharacterControllerNode,
            'BulletBoxShape':BulletBoxShape,
            'BulletPlaneShape':BulletPlaneShape,
            'BulletCapsuleShape':BulletCapsuleShape
        }
        
    def Create( self, nTypeStr, *args ):
        wrprCls = self.nodeWrappers[nTypeStr]
        return wrprCls.Create( *args )
    
    def Wrap( self, comp ):
        """
        Return a wrapper suitable for the indicated component. If the correct
        wrapper cannot be found, return a NodePath wrapper for NodePaths and
        a Base wrapper for everything else.
        """
        wrprCls = self.GetWrapper( comp )
        if wrprCls is not None:
            return wrprCls( comp )
        else:
            wrprCls = self.GetDefaultWrapper( comp )
            return wrprCls( comp )
        
    def GetDefaultWrapper( self, comp ):
        if hasattr( comp, 'getPythonTag' ):
            return self.nodeWrappers['NodePath']
        else:
            return self.nodeWrappers['Base']
        
    def GetCommonWrapper( self, comps ):
        
        # Get method resolution orders for each wrapper for all the indicated
        # components.
        mros = []
        for comp in comps:
            wrprCls = self.GetWrapper( comp )
            if wrprCls is not None:
                mros.append( wrprCls.mro() )
                
        if not mros:
            return self.GetDefaultWrapper( comp )
                
        # Intersect the mros to get the common classes.
        cmnClasses = set( mros[0] ).intersection( *mros )
        
        # The result was unordered, so go find the first common class from
        # one of the mros.
        for cls in mros[0]:
            if cls in cmnClasses:
                return cls
        
    def GetWrapper( self, comp ):
        typeStr = self.GetTypeString( comp )
        if typeStr in self.nodeWrappers:
            return self.nodeWrappers[typeStr]
        
        return None
    
    def GetWrapperByName( self, cType ):
        if cType in self.nodeWrappers:
            return self.nodeWrappers[cType]
        
        return None
        
    def GetTypeString( self, comp ):
        """
        Return the type of the component as a string. Components are 
        identified in the following method (in order):
        
        - If the component has the class variable 'cType' then this string
        will be used as the type.
        - Use the component's type's name as the type.
        - If this is 'NodePath' then look for a overriding tag on the node
        for the type.
        - If this tag is missing, use the NodePath's node as the type.
        """
        if hasattr( comp.__class__, 'cType' ):
            return comp.cType
        
        typeStr = type( comp ).__name__
        if typeStr == 'NodePath':
            typeStr = comp.node().getTag( TAG_NODE_TYPE )
            if not typeStr:
                typeStr = type( comp.node() ).__name__
                
        return typeStr