import inspect

import pandac.PandaModules as pm

from .. import gamePlugin as gp


class Script( gp.Script ):
        
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
        pandaPath = pm.Filename.fromOsSpecific( inspect.getfile( self.data.__class__ ) )
        
        relPath = pm.Filename( pandaPath )
        index = relPath.findOnSearchpath( pm.getModelPath().getValue() )
        if index >= 0:
            basePath = pm.getModelPath().getDirectories()[index]
            relPath.makeRelativeTo( basePath )
        
        return {'filePath':str( relPath )}