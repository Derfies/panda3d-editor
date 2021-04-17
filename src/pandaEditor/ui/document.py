import os

from pubsub import pub


class Document:

    def __init__(self, filePath, contents):
        self.filePath = filePath
        self.contents = contents
        
        self.dirty = False

    @property
    def title(self):
        if self.filePath is not None:
            return os.path.basename(self.filePath)
        else:
            return 'untitled'

    def load(self):
        self.contents.load(self.filePath)
        self.on_refresh()

    def save(self, **kwargs):
        filePath = kwargs.pop('filePath', self.filePath)
        self.contents.save(filePath)
        self.dirty = False
        self.on_refresh()
        
    def on_refresh(self, comps=None):
        """
        Broadcast the update message without setting the dirty flag. Methods
        subscribed to this message will rebuild ui widgets completely.
        """
        pub.sendMessage('Update', comps=comps)

    def on_modified(self, comps=None):
        """
        Broadcast the update message and set the dirty flag. Methods
        subscribed to this message will rebuild ui widgets completely.
        """
        self.dirty = True
        pub.sendMessage('Update', comps=comps)
        
    def on_selection_modified(self, task):
        """
        Broadcast the update selection message. Methods subscribed to this
        message should be quick and not force full rebuilds of ui widgets
        considering how quickly the selection is likely to change.
        """
        pub.sendMessage('SelectionModified', comps=base.selection.wrprs)
        return task.cont
