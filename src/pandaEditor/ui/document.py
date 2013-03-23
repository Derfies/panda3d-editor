import os

from wx.lib.pubsub import Publisher as pub


class Document( object ):

    def __init__( self, filePath, contents ):
        self.filePath = filePath
        self.contents = contents
        
        self.dirty = False
        self.title = self.GetTitle()
        
    def GetTitle( self ):
        if self.filePath is not None:
            return os.path.basename( self.filePath )
        else:
            return 'untitled'

    def Load( self ):
        self.contents.Load( self.filePath )
        self.OnRefresh()

    def Save( self, **kwargs ):
        filePath = kwargs.pop( 'filePath', self.filePath )
        self.contents.Save( filePath )
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
