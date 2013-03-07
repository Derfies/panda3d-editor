from camera import Camera


class BaseCam( Camera ):
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        wrpr = cls( base.cam )
        wrpr.SetupNodePath()
        return wrpr