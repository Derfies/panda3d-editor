import os

from wx.lib.pubsub import Publisher as pub


class Document( object ):

    def __init__( self, contents ):
        self.contents = contents
        
        self.dirty = False
        self.title = self.GetTitle()
        
    def GetTitle( self ):
        if self.contents.filePath is not None:
            return os.path.basename( self.contents.filePath )
        else:
            return 'untitled'

    def Load( self ):
        self.contents.Load()
        self.OnRefresh()

    def Save( self, *args ):
        self.contents.Save( *args )
        self.title = self.GetTitle()
        self.dirty = False
        self.OnRefresh()
        
    def OnRefresh( self ):
        """
        Broadcast the update message without setting the dirty flag. Methods
        subscribed to this message will rebuild ui widgets completely.
        """
        pub.sendMessage( 'Update', base.selection.nps )

    def OnModified( self, arg=None ):
        """
        Broadcast the update message and set the dirty flag. Methods
        subscribed to this message will rebuild ui widgets completely.
        """
        self.dirty = True
        pub.sendMessage( 'Update', base.selection.nps )
