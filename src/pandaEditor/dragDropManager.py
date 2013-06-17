import os

import wx


class DragDropManager( object ):
    
    def __init__( self ):
        self.app = wx.GetApp()
        self.dragElems = []
        
        # Define file types and their actions.
        self.fileTypes = {
            '.egg':self.app.AddModel,
            '.bam':self.app.AddModel,
            '.pz':self.app.AddModel,
            '.sha':self.app.AddShader#,
            #'.png':self.app.AddTexture,
            #'.tga':self.app.AddTexture,
            #'.jpg':self.app.AddTexture
        }
        
    def DoFileDrop( self, filePath, np ):
        ext = os.path.splitext( filePath )[1]
        if ext in self.fileTypes:
            fn = self.fileTypes[ext]
            fn( filePath, np )
        
    def Start( self, src, data ):
        do = wx.CustomDataObject( 'foo' )
        do.SetData( str( data ) )
        
        ds = wx.DropSource( src )
        ds.SetData( do )
        ds.DoDragDrop( wx.Drag_AllowMove )
        
        self.dragElems = []
        
    #def Validate( self, *args ):
    #    print 'val: ', args
    #    return True
    
    #def Stop( self, *args ):
    #    print args