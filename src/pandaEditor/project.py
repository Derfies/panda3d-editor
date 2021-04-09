import os
import sys
import shutil
import subprocess
import xml.etree.cElementTree as et

import pandac.PandaModules as pm
from wx.lib.pubsub import pub

import p3d
import game
import utils


PROJECT_DEF_NAME = 'project.xml'
SHADER_FILE_NAME = 'shader.sha'

SCENES = 'scenes'
MODELS = 'models'
SCRIPTS = 'scripts'
PREFABS = 'prefabs'
SHADERS = 'shaders'


class DirectoryWatcher( utils.DirectoryWatcher ):
    
    def onAdded( self, filePaths ):
        messenger.send( 'projectFilesAdded', [filePaths] )
        pub.sendMessage( 'projectFilesAdded', filePaths )
        
    def onRemoved( self, filePaths ):
        messenger.send( 'projectFilesRemoved', [filePaths] )
        pub.sendMessage( 'projectFilesRemoved', filePaths )
        
    def onModified( self, filePaths ):
        messenger.send( 'projectFilesModified', [filePaths] )
        pub.sendMessage( 'projectFilesModified', filePaths )
        

class Project( object ):
    
    def __init__( self, app ):
        self.app = app
        
        self.path = None
        self.dirs = {}
        
        # Create directory watcher
        self.dirWatcher = DirectoryWatcher()
        
    def GetProjectDefinitionPath( self ):
        return os.path.join( self.path, PROJECT_DEF_NAME )
    
    def GetMainScript( self ):
        return """from direct.directbase import DirectStart

import game


# Create game base and load level
game = game.Base()
game.OnInit()
game.Load( 'scenes/test.xml' )
run()"""
    
    def New( self, dirPath, **kwargs ):
                 
        dirs = {
            SCENES:kwargs.pop( 'scenes', 'scenes' ),
            MODELS:kwargs.pop( 'models', 'models' ),
            SCRIPTS:kwargs.pop( 'scripts', 'scripts' ),
            PREFABS:kwargs.pop( 'prefabs', 'prefabs' ),
            SHADERS:kwargs.pop( 'shaders', 'shaders' )
        }

        # Create xml tags for project directories
        rootElem = et.Element( 'Project' )
        for dirType, dirName in dirs.items():
            elem = et.SubElement( rootElem, 'Directory' )
            elem.set( 'type', dirType )
            elem.set( 'name', dirName )
        
        # Wrap with an element tree and write to file
        tree = et.ElementTree( rootElem )
        utils.Indent( tree.getroot() )
        filePath = os.path.join( dirPath, PROJECT_DEF_NAME )
        tree.write( filePath )
        
        self.path = dirPath
        
        # Create directories
        self.CreateDirectories( dirs.values() )
        
        # Create a main.py stub
        self.CreateAsset( os.path.join( dirPath, 'main.py' ), self.GetMainScript() )
    
    def Set( self, dirPath ):
        
        # Check project definition file exists
        if not os.path.exists( os.path.join( dirPath, PROJECT_DEF_NAME ) ):
            self.path = None
            return
        
        # Set the project directory
        oldPath = self.path
        self.path = dirPath
        
        # Clear the model search path and add the new project path. Make sure
        # to prepend the new directory or else Panda might search in-built
        # paths first and supply the incorrect model.
        base.ResetModelPath()
        modelPath = pm.Filename.fromOsSpecific( self.path )
        pm.getModelPath().prependDirectory( modelPath )
        
        # Remove the old project path from sys.path and add the new one
        if oldPath in sys.path:
            sys.path.remove( oldPath )
        sys.path.insert( 0, self.path )
        
        # Set paths
        self.SetDirectories()
        
        # Set directory watcher root path and start it
        self.dirWatcher.setDirectory( self.path )
        if not self.dirWatcher.running:
            self.dirWatcher.start()
        
    def CreateDirectories( self, dirNames ):
        
        # Create project directories
        for dirName in dirNames:
            os.makedirs( os.path.join( self.path, dirName ) )
            
    def SetDirectories( self ):
        """
        
        """
        self.dirs = {}
        
        projPath = self.GetProjectDefinitionPath()
        tree = et.parse( projPath )
        rootElem = tree.getroot()
        dirsElem = rootElem.findall( 'Directory' )
        for dirElem in dirsElem:
            dirName = dirElem.get( 'name' )
            dirType = dirElem.get( 'type' )
            self.dirs[dirType] = dirName
            
    def GetDirectory( self, dirType ):
        """Return the full path to the indicated directory type."""
        if self.path is not None and self.dirs:
            return os.path.join( self.path, self.dirs[dirType] )
        else:
            return None
    
    def GetScenesDirectory( self ):
        """Return the full path to the scenes directory."""
        return self.GetDirectory( SCENES )
    
    def GetModelsDirectory( self ):
        """Return the full path to the models directory."""
        return self.GetDirectory( MODELS )
    
    def GetScriptsDirectory( self ):
        """Return the full path to the scripts directory."""
        return self.GetDirectory( SCRIPTS )
    
    def GetPrefabsDirectory( self ):
        """Return the full path to the prefabs directory."""
        return self.GetDirectory( PREFABS )
    
    def GetShadersDirectory( self ):
        """Return the full path to the shaders directory."""
        return self.GetDirectory( SHADERS )
    
    def ImportAsset( self, filePath ):
        
        # Strip all extensions
        bamName = os.path.basename( filePath )
        while True:
            bamName, ext = os.path.splitext( bamName )
            if not ext:
                break
        
        # Call egg to bam and create a bam in the model directory
        modelsPath = self.GetModelsDirectory()
        tgtPath = os.path.join( modelsPath, bamName ) + '.bam'
        subprocess.call(['egg2bam', '-o', tgtPath, filePath])
    
    def GetUniqueAssetName( self, startName, dirPath ):
        """Return a unique asset name."""
        newAssetName = startName
        assetNames = os.listdir( dirPath )
        
        # Iterate until we find a incremented suffix not in use
        i = 1
        while True:
            if newAssetName not in assetNames:
                break
            baseName, ext = os.path.splitext( startName )
            newAssetName = ''.join( [baseName, str( i ), ext] )
            i += 1
            
        # Return the full path to the new asset
        return os.path.join( dirPath, newAssetName )
    
    def CreateAsset( self, filePath, contents ):
        """Base method for creating a file asset in a project folder."""
        file = open( filePath, 'w' )
        file.write( contents )
        file.close()
        
    def CreateCgShader( self ):
        """Create a new cg shader in the shaders directory."""
        dirPath = self.GetShadersDirectory()
        shaderPath = self.GetUniqueAssetName( SHADER_FILE_NAME, dirPath )
        shader = ''
        self.CreateAsset( shaderPath, shader )
        
    def GetRequiredSysPaths( self ):
        """
        Return a list of all paths needed to be on sys.path for the build
        process to run. Remember to replace backslashes with forward ones.
        """
        reqSysPaths = []
        for mod in [p3d]:
            modPath = os.path.dirname( mod.__file__ )
            modLoc = os.path.dirname( modPath ).replace( '\\', '/' )
            reqSysPaths.append( modLoc )
            
        return reqSysPaths
        
    def CreateBuildScript( self, fileName ):
        """
        Return the python script responsible for building the project. This is
        pretty inflexible at the moment, but the user should be able to change
        how this script is generated in the future with some option boxes.
        """
        # Get the path to game and add it to sys.path or the builder won't 
        # find it.
        sysPathStr = ''
        for path in self.GetRequiredSysPaths():
            sysPathStr += 'sys.path.append( \'' + path + '\' )\n'
        
        return """import sys


""" + sysPathStr + """


class """ + fileName + """( p3d ):
    require( 'morepy' )
    require( 'audio' )
    require( 'bullet' )
    mainModule( 'main' )
    dir( 'scenes', newDir='scenes' )
    dir( 'models', newDir='models' )
    dir( 'sounds', newDir='sounds' )
    dir( 'scripts', newDir='scripts' )
    dir( 'game', newDir='game' )
    dir( 'userPlugins', newDir='userPlugins' )"""
            
    def Build( self, buildPath ):
        """Build the project to a p3d file."""
        # Check if we can create a directory here with the same name as the
        # project
        tempDirPath = os.path.splitext( buildPath )[0]
        if os.path.exists( tempDirPath ):
            print('Already a directory named ', tempDirPath)
            return False
                              
        # Copy the entire project to the temp location.
        shutil.copytree( self.path, tempDirPath )
        
        # Copy the game module over to the temp project.
        gamePath = os.path.split( game.__file__ )[0]
        gameDestPath = os.path.join( tempDirPath, 'game' )
        shutil.copytree( gamePath, gameDestPath )
        
        # Now copy the plugin module.
        pluginsPath = self.app.game.pluginMgr.GetPluginsPath()
        if pluginsPath is not None:
            pluginDestPath = os.path.join( tempDirPath, 'userPlugins' )
            shutil.copytree( self.app.game.pluginMgr.GetPluginsPath(), 
                             pluginDestPath )
                             
            # Remove all editor plugins for the userPlugins directory
            for dirName in os.listdir( pluginDestPath ):
                dirPath = os.path.join( pluginDestPath, dirName )
                if os.path.isdir( dirPath ) and 'editorPlugin' in os.listdir( dirPath):
                    shutil.rmtree( os.path.join( dirPath, 'editorPlugin' ) )

        # Parse build script
        buildDirPath, buildName = os.path.split( buildPath )
        scriptLines = self.CreateBuildScript( os.path.splitext( buildName )[0] )
        buildDefPath = os.path.join( tempDirPath, 'build.pdef' )
        file = open( buildDefPath, 'w' )
        file.writelines( scriptLines )
        file.close()
        
        # Turn scripts into a module otherwise ppackage won't find it.
        scriptsPath = os.path.join( tempDirPath, 'scripts', '__init__.py' )
        file = open( scriptsPath, 'w' )
        file.close()
        
        # Run the script with ppackage, then remove the copied project once
        # it's built.
        def Cleanup():
            if os.path.exists( tempDirPath ):
                shutil.rmtree( tempDirPath )
            
        cmd = ('ppackage', '-i', buildDirPath, 'build.pdef')
        utils.PopenAndCall( Cleanup, True, cmd, stdout=subprocess.PIPE, 
                            stderr=subprocess.STDOUT, cwd=tempDirPath )
        
    def GetRelModelPath( self, pandaPath ):
        """
        Attempt to find the indicated file path on one of the model search 
        paths. If found then return a path relative to it. Also make sure to 
        remove all extensions so we can load  both egg and bam files.
        """
        relPath = pm.Filename( pandaPath )
        index = relPath.findOnSearchpath( pm.getModelPath().getValue() )
        if index >= 0:
            basePath = pm.getModelPath().getDirectories()[index]
            relPath.makeRelativeTo( basePath )
            
        # Remove all extensions
        modelPath = str( relPath )
        while True:
            modelPath, ext = os.path.splitext( modelPath )
            if not ext:
                break
        
        return modelPath