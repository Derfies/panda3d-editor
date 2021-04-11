from panda3d.core import Point3
from direct.interval.IntervalGlobal import Sequence

import p3d


class PandaWalk(p3d.PandaBehaviour):
    
    animName = str
    
    def __init__(self, *args, **kwargs):
        p3d.PandaBehaviour.__init__(self, *args, **kwargs)
        
        self.animName = ''
        
    def OnStart(self):
        
        # Find the panda actor placed in the scene.
        pandaWrpr = base.game.nodeMgr.Wrap(render.find('panda_walk_character'))
        self.pandaActor = pandaWrpr.GetActor()
        self.pandaActor.loop(self.animName)
        
        # Create the four lerp intervals needed for the panda to
        # walk back and forth.
        pandaPosInterval1 = self.pandaActor.posInterval(13,
                                                         Point3(0, -10, 0),
                                                         startPos=Point3(0, 10, 0))
        pandaPosInterval2 = self.pandaActor.posInterval(13,
                                                         Point3(0, 10, 0),
                                                         startPos=Point3(0, -10, 0))
        pandaHprInterval1 = self.pandaActor.hprInterval(3,
                                                         Point3(180, 0, 0),
                                                         startHpr=Point3(0, 0, 0))
        pandaHprInterval2 = self.pandaActor.hprInterval(3,
                                                         Point3(0, 0, 0),
                                                         startHpr=Point3(180, 0, 0))
 
        # Create and play the sequence that coordinates the intervals.
        self.pandaPace = Sequence(pandaPosInterval1,
                                   pandaHprInterval1,
                                   pandaPosInterval2,
                                   pandaHprInterval2,
                                   name='pandaPace')
        self.pandaPace.loop()
