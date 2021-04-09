import wx


class CustomDropTarget(wx.TextDropTarget):
    
    def __init__(self, formatNames, parent=None):
        super().__init__()
        
        self.app = parent.app
        self.parent = parent

        print('jere')

        # Specify the type of data we will accept
        self.doc = wx.DataObjectComposite()
        self.formats = {}
        for formatName in formatNames:
            do = wx.CustomDataObject( formatName )
            self.formats[formatName] = do
            self.doc.Add( do )
        self.SetDataObject( self.doc )

    def OnDropText(self, x, y, data):
        print('ver')
        
    def OnDragOver(self, x, y, d):

        print(x, y, d)
        
        # Return x.DragNone if the validation fails
        if not self.app.dDropMgr.ValidateDropItem(x, y, self.parent):
            return wx.DragNone
        else:
            return d
        
    def OnData( self, x, y, d ):
        
        # Copy the data from the drag source to our data object
        if self.GetData():
            
            # Call the method on the string taken from the data object
            format = self.doc.GetReceivedFormat().GetId()
            do = self.formats[format]
            self.app.dDropMgr.OnDropItem( do.GetData(), self.parent, x, y )
        
        return d