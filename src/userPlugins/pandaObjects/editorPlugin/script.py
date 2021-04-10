import panda3d.core as pm

from .. import gamePlugin as gp
from p3d import commonUtils as cUtils


class Script( gp.Script ):
        
    def GetPropertyData( self ):
        
        # Put all instance variables into a dictionary and return it.
        propDict = {'filePath':self.GetScriptPath( self.data )}
        for pName, pType in self.GetProps().items():
            propStr = cUtils.SerializeToString( getattr( self.data, pName ) )
            if propStr is not None:
                propDict[pName] = propStr
        return propDict
    
    def GetProps( self ):
        props = {}
        for pName, prop in vars( self.data.__class__ ).items():
            if type( prop ) == type:
                props[pName] = prop
                
        return props
    
    def GetScriptPath( self, data ):
        filePath = gp.Script.GetScriptPath( self, data )
        pandaPath = pm.Filename.fromOsSpecific( filePath )
        return base.project.GetRelModelPath( pandaPath )