from modelNode import ModelNode


class BaseCamera( ModelNode ):
    
    def Create( self, parent=None ):
        self.SetupNodePath( base.camera )
        self.data = base.camera
        return base.camera