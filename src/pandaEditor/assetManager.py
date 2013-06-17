import os

import panda3d.core as pc
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
            pandaPath = pm.Filename.fromOsSpecific( filePath )
            
            # Test if the file path represents an asset in one of Panda's
            # asset pools.
            if pm.TexturePool.hasTexture( pandaPath ):
                print 'Reloading texture: ', pandaPath
                self.ReloadTexture( pandaPath )
            elif pm.ModelPool.hasModel( pandaPath ):
                print 'Reloading model: ', pandaPath
                self.ReloadModel( pandaPath )
            #elif pm.ShaderPool.hasShader( pandaPath ):
            #    print 'Reloading shader: ', pandaPath
            #    self.ReloadShader( pandaPath )
        
    def ReloadTexture( self, pandaPath ):
        for tex in pm.TexturePool.findAllTextures():
            if tex.getFilename() == pandaPath:
                tex.reload()
                
    def ReloadShader( self, pandaPath ):
        pm.ShaderPool.releaseShader( pandaPath )
        loader.loadShader( pandaPath )
                
    def ReloadModel( self, pandaPath ):
        pm.ModelPool.releaseModel( pandaPath )
        pm.ModelPool.loadModel( pandaPath )
        
        # Find all instances of this model in the scene graph.
        nps = [
            np 
            for np in base.scene.rootNp.findAllMatches( '+ModelRoot' )
            if np.node().getFullpath() == pandaPath
        ]
        
        wrprCls = base.game.nodeMgr.GetWrapperByName( 'ModelRoot' )
        filePath = pm.Filename.toOsSpecific( pandaPath )
        wrpr = wrprCls.Create( modelPath=filePath )
        
        # Now unhook all the NodePaths under the ModelRoot and reparent a new
        # copy to it. This will remove all sub ModelRoot changes at the moment
        # and will need to be fixed in the future.
        oldIds = {}
        for np in nps:
            
            # Look for connections.
            inCnnctns = {}
            outCnnctns = {}
            for childNp in np.findAllMatches( '**/*' ):
                cWrpr = base.game.nodeMgr.Wrap( childNp )
                path = cWrpr.GetPath()
                oldIds[path] = cWrpr.GetId()
                for cnnctn in base.scene.GetIncomingConnections( cWrpr ):
                    # Need to break connection here?
                    inCnnctns.setdefault( path, [] )
                    inCnnctns[path].append( cnnctn )
                    
                for cnnctn in base.scene.GetOutgoingConnections( cWrpr ):
                    cnnctn.Break( cWrpr.data )
                    outCnnctns.setdefault( path, [] )
                    outCnnctns[path].append( cnnctn )
            
            # Remove the existing children.
            for childNp in np.getChildren():
                childNp.removeNode()
            
            # Copy the new updated children under the old ModelRoot NodePath
            # so we retain its properties.
            for childNp in wrpr.data.getChildren():
                cWrpr = base.game.nodeMgr.Wrap( childNp )
                dupeNp = cWrpr.Duplicate( uniqueName=False )
                dupeNp.reparentTo( np )
                
            # Replace connections.
            for childNp in np.findAllMatches( '**/*' ):
                cWrpr = base.game.nodeMgr.Wrap( childNp )
                path = cWrpr.GetPath()
                
                if path in outCnnctns:
                    for cnnctn in outCnnctns[path]:
                        cnnctn.Connect( cWrpr.data )
                        print 'Relinking: ', cnnctn.label, ' to: ', cWrpr.data
                        
                if path in inCnnctns:
                    cWrpr.SetModified( True )
                    for cnnctn in inCnnctns[path]:
                        comps = cnnctn.Get()
                        cnnctn.srcComp = childNp
                        try:
                            for comp in comps:
                                cnnctn.Connect( comp )
                        except TypeError:
                            cnnctn.Connect( comps )
                          
                        print 'Relinking: ', cnnctn.label, ' to: ', cWrpr.data
                        
                # Fix up name and ids.
                cWrpr.SetId( oldIds[path] )