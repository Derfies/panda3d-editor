import uuid

import panda3d.core as pc
import pandac.PandaModules as pm
from pandac.PandaModules import NodePath as NP

from base import Base
from constants import *
from attributes import NodePathAttribute as Attr
from game.nodes.attributes import Connection as Cnnctn
from game.nodes.attributes import ConnectionList as CnnctnList


class NodePath( Base ):
    
    type_ = NP
    
    def __init__( self, *args, **kwargs ):
        Base.__init__( self, *args, **kwargs )
        
        self.AddAttributes(
            Attr( 'Name', str, NP.getName, NP.setName ),
            Attr( 'Matrix', pm.Mat4, NP.getMat, NP.setMat ),
            CnnctnList( 'Lights', pm.Light, self.GetLights, NP.setLight, NP.clearLight, NP.clearLight ),
            Cnnctn( 'Texture', pm.Texture, NP.getTexture, NP.setTexture, NP.clearTexture, args=[1] ),
            Cnnctn( 'Shader', pc.Filename, self.GetShader, self.SetShader, NP.clearShader ),
            parent='NodePath'
        )
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        """
        Create a NodePath with the indicated type and name, set it up and
        return it.
        """
        if 'path' not in kwargs:
            if cls.initArgs is None:
                strType = cls.type_.__name__
                initArgs = [strType[0:1].lower() + strType[1:]]
            else:
                initArgs = cls.initArgs
            
            wrpr = cls( pm.NodePath( cls.type_( *initArgs ) ) )
            wrpr.SetupNodePath()
        else:
            wrpr = cls( cls.FindChild( kwargs['path'], kwargs['parent'] ) )
        return wrpr
    
    def Detach( self ):
        self.data.detachNode()
    
    def Destroy( self ):
        
        # Iterate through all addons and destroy them.
        for addon in self.GetAddons():
            addon.Destroy()
            
        self.data.removeNode()
        
    def Duplicate( self ):
        dupeNp = self.data.copyTo( self.data.getParent() )
        dupeNp.setName( self.data.getName() + '_1' )
        self.FixUpDuplicateChildren( self.data, dupeNp )
        return dupeNp
    
    def GetId( self ):
        return self.data.getTag( TAG_NODE_UUID )
        
    def SetId( self, id ):
        self.data.setTag( TAG_NODE_UUID, id )
    
    def GetParent( self ):
        return base.game.nodeMgr.Wrap( self.data.getParent() )
    
    def GetChildren( self ):
        """Return a list of wrappers for the children of this NodePath."""
        children = [
            base.game.nodeMgr.Wrap( cNp ) 
            for cNp in self.data.getChildren()
        ]
        return children
    
    def GetTags( self ):
        tags = self.data.getPythonTag( TAG_PYTHON_TAGS )
        if tags is not None:
            return [tag for tag in tags if tag in base.game.nodeMgr.nodeWrappers]
        
        return []
    
    def GetAddons( self ):
        addons = []
        
        # Add wrappers for python objects.
        for tag in self.GetTags():
            pyObj = self.data.getPythonTag( tag )
            pyObjWrpr = base.game.nodeMgr.Wrap( pyObj )
            addons.append( pyObjWrpr )
            
        return addons
    
    def OnDuplicate( self, origNp, dupeNp ):
        
        # If the original NodePath had an id then generate a new one for the 
        # duplicate.
        wrpr = base.game.nodeMgr.Wrap( origNp )
        if wrpr.GetId():
            self.CreateNewId()
            
        # Duplicate all addons / objects attached to this NodePath with python
        # tags and set them to the new NodePath.
        for tag in self.GetTags():
            pyObj = origNp.getPythonTag( tag )
            pyObjWrpr = base.game.nodeMgr.Wrap( pyObj )
            dupePyObj = pyObjWrpr.Duplicate()
            self.data.setPythonTag( tag, dupePyObj )
        
        return origNp
        
    def SetupNodePath( self ):
        self.CreateNewId()
        
    def CreateNewId( self ):
        id = str( uuid.uuid4() )
        self.data.setTag( TAG_NODE_UUID, id )
        
    def AddChild( self, np ):
        np.reparentTo( self.data )
        
    @classmethod
    def FindChild( cls, path, parent ):
        buffer = path.split( '|' )
        np = parent
        for elem in buffer:
            childNames = [child.getName() for child in np.getChildren()]
            index = childNames.index( elem )
            np = np.getChildren()[index]
                    
        return np
    
    def GetShader( self, np ):
        shader = np.getShader()
        if shader is None:
            return ''
        
        return shader.getFilename()
        
    def SetShader( self, np, filePath ):
        try:
            pandaPath = pc.Filename.fromOsSpecific( filePath )
        except TypeError:
            pandaPath = filePath
        shader = pc.Shader.load( pandaPath )
        if shader is not None:
            np.setShader( shader )
        else:
            np.clearShader()
        
    def GetLights( self, data ):
        lgts = []
        
        lgtAttrib = data.getAttrib( pm.LightAttrib )
        if lgtAttrib is not None:
            lgts = lgtAttrib.getOnLights()
        
        return lgts
    
    def GetActor( self ):
        """
        Return the actor part of this NodePath if there is one, return None
        otherwise.
        """
        return self.data.getPythonTag( TAG_ACTOR )