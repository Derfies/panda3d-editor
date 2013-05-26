import os

import pandac.PandaModules as pm


class AssetManager( object ):
    
    def __init__( self, *args, **kwargs ):
        self.assets = {}
        
    def RegisterAsset( self, assetPath, asset ):
        self.assets.setdefault( assetPath, [] )
        self.assets[assetPath].append( asset )
        
    def OnAssetModified( self, filePaths ):
        """
        Reload the indicated file paths as they have been marked as dirty in
        the project directory.
        """
        for filePath in filePaths:
            
            # Bail if the path is a directory.
            if os.path.isdir( filePath ):
                continue
            
            # Test if the file path represents a texture in the texture pool.
            pandaPath = pm.Filename.fromOsSpecific( filePath )
            if pm.TexturePool.hasTexture( pandaPath ):
                self.ReloadTexture( pandaPath )
        
    def ReloadTexture( self, pandaPath ):
        for tex in pm.TexturePool.findAllTextures():
            if tex.getFilename() == pandaPath:
                print 'Reloading: ', tex.getFilename()
                tex.reload()