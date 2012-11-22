import os

import pandac.PandaModules as pm

import p3d
from game.plugins.base import Base


class EditorPlugin( Base ):
        
    def OnInit( self ):
        Base.OnInit( self )
        
        # Set editor meshes.
        nWrprs = self.app.game.nodeMgr.nodeWrappers
        nWrprs['BaseCam'].SetEditorGeometry( loader.loadModel( self.GetModelPath( 'Camera.egg' ) ) )
        nWrprs['PointLight'].SetEditorGeometry( loader.loadModel( self.GetModelPath( 'PointLight.egg' ) ) )
        
    def GetModelPath( self, fileName ):
        """
        Return the model path for the specified file name. Model paths are
        given as absolute paths so there is not need to alter the model search
        path - doing so may give weird results if there is a similarly named
        model in the user's project.
        """
        dirPath = os.path.join( os.path.split( __file__ )[0], 'models' )
        modelPath = pm.Filename.fromOsSpecific( os.path.join( dirPath, fileName ) )
        return modelPath