import os

import panda3d.core as pm
from panda3d.core import Shader

import p3d
from game.plugins.base import Base


class EditorPlugin(Base):
        
    def OnInit(self):
        Base.OnInit(self)
        
        # Load vertex colour shader.
        vtxShader = Shader.load(self.GetModelPath('vertexColours.sha'))
        
        # Set editor meshes.
        modelWrprMap = {
            'Camera.egg':'BaseCam',
            'AmbientLight.egg':'AmbientLight',
            'Spotlight.egg':'Spotlight',
            'PointLight.egg':'PointLight',
            'DirectionalLight.egg':'DirectionalLight'
        }
        for modelName, wrprName in modelWrprMap.items():
            model = loader.loadModel(self.GetModelPath(modelName))
            model.setShader(vtxShader)
            self.app.game.nodeMgr.nodeWrappers[wrprName].SetEditorGeometry(model)
        
    def GetModelPath(self, fileName):
        """
        Return the model path for the specified file name. Model paths are
        given as absolute paths so there is not need to alter the model search
        path - doing so may give weird results if there is a similarly named
        model in the user's project.
        """
        dirPath = os.path.join(os.path.split(__file__)[0], 'models')
        modelPath = pm.Filename.fromOsSpecific(os.path.join(dirPath, fileName))
        return modelPath