import p3d
from base import Base


class Remove( Base ):
    
    def __init__( self, app, nps ):
        self.app = app
        self.nps = nps
    
    def Undo( self ):
        self.app.scene.AddNodePaths( self.nps )
        self.app.doc.OnModified()
    
    def Redo( self ):
        self.app.scene.DeleteNodePaths( self.nps )
        self.app.doc.OnModified()