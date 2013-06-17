import os
import copy
import inspect

import wx

import p3d
import game
from constants import *
from game.nodes.base import Base
from game.nodes import Attribute as Attr


class PandaObjectNPO( p3d.NodePathObject ):
    
    cType = TAG_PANDA_OBJECT
    pyTagName = TAG_PANDA_OBJECT
    
    def __init__( self ):
        self.instances = {}
    

class PandaObject( Base ):
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        return cls( PandaObjectNPO() )
    
    def Detach( self ):
        
        # Remove the NodePath's tag referencing the PandaObject. Also remove
        # the PandaObject tag from the list of tags on this NodePath.
        self.data.np.clearPythonTag( TAG_PANDA_OBJECT )
        pyTag = self.data.np.getPythonTag( game.nodes.TAG_PYTHON_TAGS )
        if pyTag is not None:
            pyTag.remove( TAG_PANDA_OBJECT )
    
    def Destroy( self ):
        for clsName, instance in self.data.instances.items():
            filePath = inspect.getfile( instance.__class__ )
            try:
                instance.ignoreAll()
            except Exception, e:
                print 'Could not ignore: ', e
            del self.data.instances[clsName]

        PandaObjectNPO.Break( self.data.np )
        
        self.data = None
        
    def Duplicate( self ):
        dupePyObj = copy.copy( self.data )
        self.FixUpDuplicateChildren( self.data, dupePyObj )
        return dupePyObj
        
    def SetId( self, id ):
        
        # PandaObjects don't need ids.
        pass
    
    def GetType( self ):
        #print 'using: ', TAG_PANDA_OBJECT
        return TAG_PANDA_OBJECT
        
    def GetParent( self ):
        return base.game.nodeMgr.Wrap( self.data.np )
    
    def SetParent( self, pNp ):
        if pNp is None:
            return
        
        self.data.Attach( pNp )
        
        pyTag = pNp.getPythonTag( game.nodes.TAG_PYTHON_TAGS )
        if pyTag is None:
            pyTag = []
            pNp.setPythonTag( game.nodes.TAG_PYTHON_TAGS, pyTag )
            
        if TAG_PANDA_OBJECT not in pyTag:
            pyTag.append( TAG_PANDA_OBJECT )
            
    def GetChildren( self ):
        children = []
        
        # Create wrappers for each script attached to the object.
        wrprCls = base.game.nodeMgr.nodeWrappers['Script']
        for name, instance in self.data.instances.items():
            children.append( wrprCls( instance ) )
            
        return children
    
    def GetAttributes( self, *args, **kwargs ):
        attrs = []
        
        if self.data is not None:
            for name, instance in self.data.instances.items():
                for pName, pType in self.GetProps( instance ).items():
                    attrs.append( Attr( pName, pType, getattr, setattr, 
                                        self.GetPObjInstance, [pName], [pName], 
                                        [name], w=False, parent=name,
                                        srcComp=self.data ) )
        
        return attrs
    
    def GetPObjInstance( self, pObj, clsName ):
        return pObj.instances[clsName]
    
    def GetProps( self, instance ):
        props = {}
        for pName, prop in vars( instance.__class__ ).items():
            if type( prop ) == type:
                props[pName] = prop
                
        return props
    
    def ReloadScript( self, scriptPath ):
        
        # Get the class name
        head, tail = os.path.split( scriptPath )
        name = os.path.splitext( tail )[0]
        clsName = name[0].upper() + name[1:]
        
        # Get the current script instance, detach it from the PandaObject and
        # delete it.
        script = self.data.instances[clsName]
        scriptWrpr = base.game.nodeMgr.Wrap( script )
        scriptWrpr.Detach()
        del scriptWrpr.data
        
        try:
            scriptWrprCls = base.game.nodeMgr.nodeWrappers['Script']
            scriptWrpr = scriptWrprCls.Create( filePath=scriptPath )
        except:
            wxUtils.ErrorDialog( traceback.format_exc(), 'Script Error' )
            return
        
        scriptWrpr.SetParent( self.data )
        
    def OnDuplicate( self, origComp, dupeComp ):
        dupeComp.instances = {}
        for name, instance in origComp.instances.items():
            dupeComp.instances[name] = copy.copy( instance )    