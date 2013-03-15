import inspect

import pandac.PandaModules as pm

import p3d
from .. import gamePlugin as gp


class Script( gp.Script ):
    
    def GetParent( self ):
        return p3d.PandaObject.Get( self.data.np )
        
    def GetPropertyData( self ):
        
        # Put all instance variables into a dictionary and return it.
        dataDict = {}
        for pName, pType in self.GetProps().items():
            dataDict[pName] = getattr( self.data, pName )
        return dataDict
    
    def GetProps( self ):
        props = {}
        for pName, prop in vars( self.data.__class__ ).items():
            if type( prop ) == type:
                props[pName] = prop
                
        return props
    
    def GetCreateArgs( self ):
        filePath = inspect.getfile( self.data.__class__ )
        pandaPath = pm.Filename.fromOsSpecific( filePath )
        relPath = base.project.GetRelModelPath( pandaPath )
        return {'filePath':str( relPath )}