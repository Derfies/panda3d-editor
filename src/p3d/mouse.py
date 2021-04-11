from p3d.singleTask import SingleTask


MOUSE_ALT = 0
MOUSE_CTRL = 1


class Mouse(SingleTask):
    
    """Class representing the mouse."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.buttons = [False, False, False]
        self.modifiers = []
        
        # Bind button events
        self.accept('alt', self.SetModifier, [MOUSE_ALT])
        self.accept('alt-up', self.ClearModifier, [MOUSE_ALT])
        self.accept('control', self.SetModifier, [MOUSE_CTRL])
        self.accept('control-up', self.ClearModifier, [MOUSE_CTRL])
        
        self.accept('alt-mouse1', self.SetButton, [0, True])
        self.accept('control-mouse1', self.SetButton, [0, True])
        self.accept('mouse1', self.SetButton, [0, True])
        self.accept('mouse1-up', self.SetButton, [0, False])
        
        self.accept('alt-mouse2', self.SetButton, [1, True])
        self.accept('control-mouse2', self.SetButton, [1, True])
        self.accept('mouse2', self.SetButton, [1, True])
        self.accept('mouse2-up', self.SetButton, [1, False])
        
        self.accept('alt-mouse3', self.SetButton, [2, True])
        self.accept('control-mouse3', self.SetButton, [2, True])
        self.accept('mouse3', self.SetButton, [2, True])
        self.accept('mouse3-up', self.SetButton, [2, False])
            
    def OnUpdate(self, task):
        
        # Get pointer from screen, calculate delta
        mp = self.win.getPointer(0)
        self.dx = self.x - mp.getX()
        self.dy = self.y - mp.getY()
        self.x = mp.getX()
        self.y = mp.getY()
        
    def SetModifier(self, modifier):
        
        # Record modifier
        if modifier not in self.modifiers:
            self.modifiers.append(modifier)
        
    def ClearModifier(self, modifier):
        
        # Remove modifier
        if modifier in self.modifiers:
            self.modifiers.remove(modifier)
        
    def SetButton(self, id, value):
        
        # Record button value
        self.buttons[id] = value