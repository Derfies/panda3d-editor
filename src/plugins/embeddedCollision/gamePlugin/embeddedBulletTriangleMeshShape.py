import uuid
import copy

import panda3d.bullet as blt
import panda3d.core as pm

import p3d
import game
from .constants import *
from game.nodes.constants import *
#from editor.nodes.constants import *
from game.nodes.nodePath import NodePath
from game.nodes.collisionNode import CollisionNode
from game.nodes.bulletRigidBodyNode import BulletRigidBodyNode


class EmbeddedBulletTriangleMeshShape(BulletRigidBodyNode):
    
    def __init__(self, *args, **kwargs):
        BulletRigidBodyNode.__init__(self, *args, **kwargs)
        
        # Remove the shapes connection as this is built from the input 
        # NodePath.
        #self.attributes.
        cnnctn = self.FindProperty('shapes')
        self.attributes.remove(cnnctn)
    
    @classmethod
    def Create(cls, *args, **kwargs):
        if 'inputNp' in kwargs:
            inputNp = kwargs['inputNp']
        elif 'path' in kwargs:
            inputNp = cls(cls.FindChild(kwargs['path'], kwargs['parent']))
            return inputNp
        else:
            return cls(pm.NodePath(blt.BulletRigidBodyNode('')))
        
        # Get all geom nodes at this level and below.
        #geomNps = inputNp.findAllMatches('**/+GeomNode')
        #if inputNp.node().isOfType(pm.GeomNode):
        #    geomNps.addPath(inputNp)
        
        geomNps = [inputNp]
            
        # Get a flat list of all geoms.
        geoms = []
        for geomNp in geomNps:
            geoms.extend(geomNp.node().getGeoms())
            
        mesh = blt.BulletTriangleMesh()
        for geom in geoms:
            mesh.addGeom(geom)
            
        shape = blt.BulletTriangleMeshShape(mesh, dynamic=False)
        rBody = blt.BulletRigidBodyNode(inputNp.getName())
        rBody.addShape(shape)
        
        # Swap the original NodePath for the one we just created.
        np = pm.NodePath(rBody)
        np.reparentTo(inputNp.getParent())
        np.setTag(game.nodes.TAG_NODE_TYPE, TAG_EMBEDDED_BULLET_TRIANGLE_MESH_SHAPE)
        
        inputNp.detachNode()
        wrpr = cls(np)
        wrpr.CreateNewId()
        
        return wrpr
    
    def OnDuplicate(self, origNp, dupeNp):
        
        # Duplicate doesn't work for rigid body nodes...
        foo = blt.BulletRigidBodyNode(origNp.getName())
        bar = pm.NodePath(foo)
        bar.reparentTo(self.data.getParent())
        self.data.detachNode()
        
        self.data = bar
        self.data.setTag(game.nodes.TAG_NODE_TYPE, TAG_EMBEDDED_BULLET_TRIANGLE_MESH_SHAPE)
        #self.SetupNodePath()
        for shape in origNp.node().getShapes():
            copShape = copy.copy(shape)
            self.data.node().addShape(copShape)
        
        BulletRigidBodyNode.OnDuplicate(self, origNp, dupeNp)
        
        return self.data
        