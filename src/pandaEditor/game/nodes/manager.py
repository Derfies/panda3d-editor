from game.nodes.actor import Actor
from game.nodes.base import Base
from game.nodes.bullet import (
    BulletBoxShape,
    BulletCapsuleShape,
    BulletCharacterControllerNode,
    BulletDebugNode,
    BulletPlaneShape,
    BulletRigidBodyNode,
    BulletWorld,
)
from game.nodes.camera import Camera
from game.nodes.collision import (
    CollisionBox,
    CollisionInvSphere,
    CollisionNode,
    CollisionRay,
    CollisionSphere,
    CollisionTube,
)
from game.nodes.constants import TAG_NODE_TYPE
from game.nodes.fog import Fog
from game.nodes.lensnode import LensNode
from game.nodes.lights import (
    AmbientLight,
    DirectionalLight,
    PointLight,
    Spotlight
)
from game.nodes.modelnode import ModelNode
from game.nodes.modelroot import ModelRoot
from game.nodes.nodepath import NodePath
from game.nodes.pandanode import PandaNode
from game.nodes.sceneroot import SceneRoot
from game.nodes.showbasedefaults import (
    Aspect2d,
    BaseCam,
    BaseCamera,
    Cam2d,
    Camera2d,
    Pixel2d,
    Render,
    Render2d,
)


class Manager:
    
    def __init__(self):
        self.wrappers = {
            'Actor': Actor,
            'AmbientLight': AmbientLight,
            'Aspect2d': Aspect2d,
            'Base': Base,
            'BaseCam': BaseCam,
            'BaseCamera': BaseCamera,
            'BulletBoxShape': BulletBoxShape,
            'BulletCapsuleShape': BulletCapsuleShape,
            'BulletCharacterControllerNode': BulletCharacterControllerNode,
            'BulletDebugNode': BulletDebugNode,
            'BulletPlaneShape': BulletPlaneShape,
            'BulletRigidBodyNode': BulletRigidBodyNode,
            'BulletWorld': BulletWorld,
            'Cam2d': Cam2d,
            'Camera': Camera,
            'Camera2d': Camera2d,
            'CollisionBox': CollisionBox,
            'CollisionInvSphere': CollisionInvSphere,
            'CollisionNode': CollisionNode,
            'CollisionRay': CollisionRay,
            'CollisionSphere': CollisionSphere,
            'CollisionTube': CollisionTube,
            'DirectionalLight': DirectionalLight,
            'Fog': Fog,
            'LensNode': LensNode,
            'ModelNode': ModelNode,
            'ModelRoot': ModelRoot,
            'NodePath': NodePath,
            'PandaNode': PandaNode,
            'Pixel2d': Pixel2d,
            'PointLight': PointLight,
            'Render': Render,
            'Render2d': Render2d,
            'SceneRoot': SceneRoot,
            'Spotlight': Spotlight,
        }
        
    def create(self, nTypeStr, *args):
        wrprCls = self.wrappers[nTypeStr]
        return wrprCls.create(*args)
    
    def wrap(self, comp):
        """
        Return a wrapper suitable for the indicated component. If the correct
        wrapper cannot be found, return a NodePath wrapper for NodePaths and
        a Base wrapper for everything else.
        """
        wrprCls = self.GetWrapper(comp)
        if wrprCls is not None:
            return wrprCls(comp)
        else:
            wrprCls = self.GetDefaultWrapper(comp)
            return wrprCls(comp)
        
    def GetDefaultWrapper(self, comp):
        if hasattr(comp, 'getPythonTag'):
            return self.wrappers['NodePath']
        else:
            return self.wrappers['Base']
        
    def GetWrapper(self, comp):
        type_ = self.GetTypeString(comp)
        return self.wrappers.get(type_)
    
    def GetWrapperByName(self, c_type):
        return self.wrappers.get(c_type)
        
    def GetTypeString(self, comp):
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
        if hasattr(comp.__class__, 'cType'):
            return comp.cType
        
        typeStr = type(comp).__name__
        if typeStr == 'NodePath':
            #print('IS EMPTY:', comp.get_name())
            typeStr = comp.node().get_tag(TAG_NODE_TYPE)
            if not typeStr:
                typeStr = type(comp.node()).__name__
                
        return typeStr