from modelNode import ModelNode


class BaseCamera( ModelNode ):
    
    def Create( self ):
        self.SetupNodePath( base.camera )
        self.Wrap( base.camera )
        return base.camera