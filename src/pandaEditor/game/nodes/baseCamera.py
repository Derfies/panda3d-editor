from modelNode import ModelNode


class BaseCamera( ModelNode ):
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        wrpr = cls( base.camera )
        wrpr.SetupNodePath()
        return wrpr