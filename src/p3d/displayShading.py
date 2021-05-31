from direct.showbase.DirectObject import DirectObject


class DisplayShading(DirectObject):
    
    """Toggles display shading."""
        
    def SetWireframe(self, value):
        if value:
            base.wireframeOn()
        else:
            base.wireframeOff()
            
    def SetTexture(self, value):
        if value:
            base.textureOn()
        else:
            base.textureOff()

    def Wireframe(self):
        self.SetWireframe(True)
        self.SetTexture(False)
    
    def Shade(self):
        self.SetWireframe(False)
        self.SetTexture(False)

    def Texture(self):
        self.SetWireframe(False)
        self.SetTexture(True)