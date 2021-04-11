import os
import weakref


class PandaManager:
    
    PANDA_BEHAVIOUR_INIT = 'PandaBehaviourInit'
    PANDA_BEHAVIOUR_START = 'PandaBehaviourStart'
    PANDA_BEHAVIOUR_STOP = 'PandaBehaviourStop'
    PANDA_BEHAVIOUR_DEL = 'PandaBehaviourDel'
    
    def __init__(self):
        
        if not hasattr(self, 'initialised'):
            self.pObjs = {}
            
            # Set initialise flag
            self.initialised = True
    
    def Init(self):
        messenger.send(self.PANDA_BEHAVIOUR_INIT)
        
    def Start(self):
        messenger.send(self.PANDA_BEHAVIOUR_START)
        
    def Stop(self):
        messenger.send(self.PANDA_BEHAVIOUR_STOP)
        
    def Del(self):
        messenger.send(self.PANDA_BEHAVIOUR_DEL)
        
    def RegisterScript(self, filePath, pObj):
        """
        Register the script and the instance. Make sure to register the .py 
        file, not a .pyo or .pyc file.
        """
        filePath = os.path.splitext(filePath)[0]# + '.py'
        self.pObjs.setdefault(filePath, weakref.WeakSet([]))
        self.pObjs[filePath].add(pObj)
        
    def DeregisterScript(self, scriptPath):
        filePath = os.path.splitext(scriptPath)[0]
        if filePath in self.pObjs:
            print('degister: ', filePath)
            del self.pObjs[filePath]
        else:
            print('couldnt find: ', filePath)
        
    def ReloadScripts(self, scriptPaths):
        """
        Reload the scripts at the indicated file paths. This means reloading
        the code and also recreating any objects that were attached to node
        paths in the scene.
        """
        scriptPaths = set(scriptPaths) & set(self.pObjs.keys())
        for scriptPath in scriptPaths:
            print('Reloading script: ', scriptPath)
            for pObj in self.pObjs[scriptPath]:
                pObjWrpr = base.game.nodeMgr.Wrap(pObj)
                pObjWrpr.ReloadScript(scriptPath)