from direct.showbase.DirectObject import DirectObject


class FrameRate(DirectObject):
    
    """Toggles displaying the framerate with F12."""
    
    def __init__(self):
        self.state = False
        self.accept('f12', self.Toggle)

    def Toggle(self):
        self.state = not self.state
        getBase().setFrameRateMeter(self.state)