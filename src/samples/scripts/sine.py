import math

import p3d


class Sine( p3d.PandaBehaviour ):
    
    amplitude = float
    
    def __init__( self, *args, **kwargs ):
        p3d.PandaBehaviour.__init__( self, *args, **kwargs )
        
        self.amplitude = 10
    
    def OnUpdate( self, task ):
        self.np.setZ( math.sin( task.time ) * self.amplitude )
