import os
import sys
import traceback


class Manager( object ):
    
    def __init__( self, game ):
        self.game = game
        
        self.plugins = []
    
    def LoadPlugin( self, fileName ):
        try:
            mod = __import__( fileName )
            cls = getattr( mod.gamePlugin, 'GamePlugin' )
            return cls( self.game )
        except Exception:
            traceback.print_exc()
            return None
            
    def GetPluginsPath( self ):
        """
        Attempt to import plugins directory. Return None if it wasn't found.
        """
        try:
            import userPlugins
        except ImportError:
            print('Failed to load plugins.')
            return None

        return os.path.split( userPlugins.__file__ )[0]
        
    def Load( self ):
        """Attempt to load plugins from their directory."""
        # Put the plugins directory on sys.path.
        pluginsPath = self.GetPluginsPath()
        if pluginsPath is None:
            return
        
        if pluginsPath not in sys.path:
            sys.path.insert( 0, pluginsPath )
        
        print('Using plugins path: ', pluginsPath)
        
        # Load all plugins
        for fileName in os.listdir( pluginsPath ):
            filePath = os.path.join( pluginsPath, fileName )
            if os.path.isdir( filePath ):
                plugin = self.LoadPlugin( fileName )
                if plugin is not None:
                    self.plugins.append( plugin )
            
        # Now run their OnInit methods
        self.SortPlugins()
        for plugin in self.plugins:
            plugin.OnInit()
            
    def SortPlugins( self ):
        """Sort plugins by accending sort order."""
        self.plugins = sorted( self.plugins, key=lambda plugin: plugin._sort )
            
    def OnNodeDuplicate( self, np ):
        for plugin in self.plugins:
            plugin.OnNodeDuplicate( np )
    
    def OnNodeDestroy( self, np ):
        for plugin in self.plugins:
            plugin.OnNodeDestroy( np )