import traceback

import game


class Manager( game.plugins.Manager ):
    
    def __init__( self, *args, **kwargs ):
        game.plugins.Manager.__init__( self, *args, **kwargs )
        
    def LoadPlugin( self, fileName ):
        temp = __import__( fileName, globals(), locals(), ['editorPlugin'], -1 )
        
        # Create an instance of the editor plugin to wrap the game plugin.
        try:
            cls = getattr( temp.editorPlugin, 'EditorPlugin' )
            return cls( self.game )
        except Exception, e:
            traceback.print_exc()
        
    def OnSceneClose( self ):
        for plugin in self.plugins:
            plugin.OnSceneClose()
            
    def OnUpdate( self, msg ):
        for plugin in self.plugins:
            plugin.OnUpdate( msg )
            
    def OnProjectFilesModified( self, filePaths ):
        for plugin in self.plugins:
            plugin.OnProjectFilesModified( filePaths )