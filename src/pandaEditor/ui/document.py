import os

import wx
from wx.lib.pubsub import Publisher as pub

import pandaEditor


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
        
    def OnSelectionChanged( self ):
        """
        Broadcast the update selection message. Methods subscribed to this
        message should be quick and not force full rebuilds of ui widgets
        considering how quickly the selection is likely to change.
        """
        pub.sendMessage( 'UpdateSelection', wx.GetApp().selection.nps )
        
    def OnSelectionModified( self, task ):
        
        pub.sendMessage( 'SelectionModified', wx.GetApp().selection.nps )
        return task.cont

    def OnRefresh( self ):
        """
        Broadcast the update message without setting the dirty flag. Methods
        subscribed to this message will rebuild ui widgets completely.
        """
        pub.sendMessage( 'Update', self )

    def OnModified( self ):
        """
        Broadcast the update message and set the dirty flag. Methods
        subscribed to this message will rebuild ui widgets completely.
        """
        self.dirty = True
        pub.sendMessage( 'Update', self )
