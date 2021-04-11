import os

from pubsub import pub


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
        
    def OnRefresh( self, comps=None ):
        """
        Broadcast the update message without setting the dirty flag. Methods
        subscribed to this message will rebuild ui widgets completely.
        """
        pub.sendMessage( 'Update', comps=comps )

    def OnModified(self, comps=None):
        """
        Broadcast the update message and set the dirty flag. Methods
        subscribed to this message will rebuild ui widgets completely.
        """
        self.dirty = True
        pub.sendMessage('Update', comps=comps)
        
    def OnSelectionModified( self, task ):
        """
        Broadcast the update selection message. Methods subscribed to this
        message should be quick and not force full rebuilds of ui widgets
        considering how quickly the selection is likely to change.
        """
        pub.sendMessage( 'SelectionModified', comps=base.selection.wrprs )
        return task.cont
