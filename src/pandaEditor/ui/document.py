import os

from direct.showbase.PythonUtil import getBase as get_base
from pubsub import pub


class Document:

    def __init__(self, file_path, contents):
        self.file_path = file_path
        self.contents = contents
        
        self.dirty = False

    @property
    def title(self):
        if self.file_path is not None:
            return os.path.basename(self.file_path)
        else:
            return 'untitled'

    def load(self):
        self.contents.load(self.file_path)
        self.on_refresh()

    def save(self, **kwargs):
        file_path = kwargs.pop('file_path', self.file_path)
        self.contents.save(file_path)
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
        pub.sendMessage('SelectionModified', comps=get_base().selection.comps)
        return task.cont
