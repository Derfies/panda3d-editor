from game.nodes.attributes import NodePathAttribute
from pandaEditor.nodes.constants import TAG_IGNORE


TAG_FRUSTUM = 'P3D_Fustum'


class LensNode:
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        i = self.attributes.index(self.FindProperty('fov'))
        self.AddAttributes(NodePathAttribute('Show Frustum', bool, self.GetFrustumVisible, self.SetFrustumVisible, w=False), index=i + 1)
        
    def OnSelect(self):
        """
        Selection handler. Make sure to disable the frustum if it was shown
        before running the select handler as the frustum will change the size
        of the bounding box.
        """
        frusVis = self.GetFrustumVisible(self.data)
        if frusVis:
            self.SetFrustumVisible(self.data, False)
            
        super().OnSelect()
        
        if frusVis:
            self.SetFrustumVisible(self.data, True)
        
    def GetFrustumVisible(self, np):
        """
        Return True if the lens node's frustum is visible, False otherwise.
        """
        visible = False
        
        children = set(np.getChildren())
        for child in children:
            if child.getPythonTag(TAG_FRUSTUM):
                visible = True
                        
        return visible
        
    def SetFrustumVisible(self, np, val):
        """
        Set the camera's frustum to be visible. Ensure it is tagged for 
        removal and also so it doesn't appear in any of the scene graph 
        panels.
        """
        if val:
            children = set(np.getChildren())
            np.node().showFrustum()
            frustum = list(set(np.getChildren()) - children)[0]
            frustum.setPythonTag(TAG_FRUSTUM, True)
            frustum.setPythonTag(TAG_IGNORE, True)
        else:
            np.node().hideFrustum()
