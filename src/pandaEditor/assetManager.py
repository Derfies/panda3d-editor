import logging
import os

import panda3d.core as pm
from direct.showbase.PythonUtil import getBase as get_base


logger = logging.getLogger(__name__)


class AssetManager:
    
    def __init__(self, *args, **kwargs):
        self.assets = {}
        
    def RegisterAsset(self, assetPath, asset):
        self.assets.setdefault(assetPath, [])
        self.assets[assetPath].append(asset)
        
    def OnAssetModified(self, filePaths):
        """
        Reload the indicated file paths as they have been marked as dirty in
        the project directory.
        """
        for filePath in filePaths:
            
            # Bail if the path is a directory.
            if os.path.isdir(filePath):
                continue
            pandaPath = pm.Filename.fromOsSpecific(filePath)
            
            # Test if the file path represents an asset in one of Panda's
            # asset pools.
            if pm.TexturePool.hasTexture(pandaPath):
                logger.info('Reloading texture: ', pandaPath)
                self.ReloadTexture(pandaPath)
            elif pm.ModelPool.hasModel(pandaPath):
                logger.info('Reloading model: ', pandaPath)
                self.ReloadModel(pandaPath)
            #elif pm.ShaderPool.hasShader(pandaPath):
            #    print 'Reloading shader: ', pandaPath
            #    self.ReloadShader(pandaPath)
        
    def ReloadTexture(self, pandaPath):
        for tex in pm.TexturePool.findAllTextures():
            if tex.getFilename() == pandaPath:
                tex.reload()
                
    def ReloadShader(self, pandaPath):
        pm.ShaderPool.releaseShader(pandaPath)
        loader.loadShader(pandaPath)
                
    def ReloadModel(self, pandaPath):
        pm.ModelPool.releaseModel(pandaPath)
        pm.ModelPool.loadModel(pandaPath)
        
        # Find all instances of this model in the scene graph.
        nps = [
            np 
            for np in get_base().scene.rootNp.findAllMatches('**/+ModelRoot')
            if np.node().getFullpath() == pandaPath
        ]
        
        wrprCls = get_base().node_manager.get_component_by_name('ModelRoot')
        filePath = pm.Filename.toOsSpecific(pandaPath)
        wrpr = wrprCls.create(model_path=filePath)
        
        # Now unhook all the NodePaths under the ModelRoot and reparent a new
        # copy to it. This will remove all sub ModelRoot changes at the moment
        # and will need to be fixed in the future.
        oldIds = {}
        for np in nps:
            
            # Look for connections.
            inCnnctns = {}
            outCnnctns = {}
            for childNp in np.findAllMatches('**/*'):
                cWrpr = get_base().node_manager.wrap(childNp)
                path = cWrpr.get_path()
                oldIds[path] = cWrpr.id
                for cnnctn in get_base().scene.get_incoming_connections(cWrpr):
                    # Need to break connection here?
                    inCnnctns.setdefault(path, [])
                    inCnnctns[path].append(cnnctn)
                    
                for cnnctn in get_base().scene.get_outgoing_connections(cWrpr):
                    cnnctn.clear(cWrpr.data)
                    outCnnctns.setdefault(path, [])
                    outCnnctns[path].append(cnnctn)
            
            # Remove the existing children.
            for childNp in np.getChildren():
                childNp.removeNode()
            
            # Copy the new updated children under the old ModelRoot NodePath
            # so we retain its properties.
            for childNp in wrpr.data.getChildren():
                cWrpr = get_base().node_manager.wrap(childNp)
                dupeNp = cWrpr.duplicate(unique_name=False)
                dupeNp.reparentTo(np)
                
            # Replace connections.
            for childNp in np.findAllMatches('**/*'):
                cWrpr = get_base().node_manager.wrap(childNp)
                path = cWrpr.get_path()
                
                if path in outCnnctns:
                    for cnnctn in outCnnctns[path]:
                        cnnctn.connect(cWrpr.data)
                        #print 'Relinking: ', cnnctn.label, ' to: ', cWrpr.data
                        
                if path in inCnnctns:
                    cWrpr.modified = True
                    for cnnctn in inCnnctns[path]:
                        comps = cnnctn.Get()
                        cnnctn.srcComp = childNp
                        try:
                            for comp in comps:
                                cnnctn.connect(comp)
                        except TypeError:
                            cnnctn.connect(comps)
                          
                        #print 'Relinking: ', cnnctn.label, ' to: ', cWrpr.data
                        
                # Fix up name and ids.
                cWrpr.set_id(oldIds[path])
