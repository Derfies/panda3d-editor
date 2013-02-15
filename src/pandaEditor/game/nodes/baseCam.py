from camera import Camera


class BaseCam( Camera ):
    
    def Create( self, parent=None ):
        self.SetupNodePath( base.cam )
        self.data = base.cam
        return base.cam