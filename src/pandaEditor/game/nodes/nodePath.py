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
        Base.Destroy( self )
        
        base.game.pluginMgr.OnNodeDestroy( self.data )
        
    def Duplicate( self, np, dupeNp ):
        Base.Duplicate( self, np, dupeNp )
        
        for child in self.children:
            child.Duplicate( np, dupeNp )
        base.game.pluginMgr.OnNodeDuplicate( self.data )
        
        # Give a new uuid to the duplicate node.
        dupeWrpr = base.game.nodeMgr.Wrap( dupeNp )
        dupeWrpr.SetupNodePath()
        
    def SetupNodePath( self ):
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