from camera import Camera


class BaseCam( Camera ):
    
    def Create( self ):
        self.SetupNodePath( base.cam )
        self.Wrap( base.cam )
        return base.cam