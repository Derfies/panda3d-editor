import wx


class CustomDropTarget(wx.TextDropTarget):
    
    def __init__(self, base, parent, formatNames):
        super().__init__()

        self.base = base
        self.parent = parent

        # Specify the type of data we will accept
        self.doc = wx.DataObjectComposite()
        self.formats = {}
        for formatName in formatNames:
            do = wx.CustomDataObject(formatName)
            self.formats[formatName] = do
            self.doc.Add(do)
        self.SetDataObject(self.doc)
        
    def OnDragOver(self, x, y, d):
        
        # Return x.DragNone if the validation fails
        if not self.base.drag_drop_manager.ValidateDropItem(x, y, self.parent):
            return wx.DragNone
        else:
            return d
        
    def OnData(self, x, y, d):
        
        # Copy the data from the drag source to our data object
        if self.GetData():
            
            # Call the method on the string taken from the data object
            format = self.doc.GetReceivedFormat().GetId()
            do = self.formats[format]
            self.base.drag_drop_manager.OnDropItem(do.GetData(), self.parent, x, y)
        
        return d
