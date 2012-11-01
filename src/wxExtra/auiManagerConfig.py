import wx


class AuiManagerConfig( wx.Config ):
    
    """
    Custom wxConfig class to handle the main frame size and position, plus all
    the the panes of the aui.
    """
    
    def __init__( self, auiMgr, *args, **kwargs ):
        wx.Config.__init__( self, *args, **kwargs )
        
        self.auiMgr = auiMgr
        self.win = self.auiMgr.GetManagedWindow()
        
        # Key constants
        if self.win is not None:
            winName = self.win.GetName()
            self._keyWinPosX = winName + 'PosX'
            self._keyWinPosY = winName + 'PosY'
            self._keyWinSizeX = winName + 'SizeX'
            self._keyWinSizeY = winName + 'SizeY'
            self._keyWinMax = winName + 'Max'
            self._keyPerspDefault = 'perspDefault'
        
    def Save( self ):
        """Save all panel layouts for the aui manager."""
        # Get old window position and size. We'll use these instead of the
        # maximized window's size and position.
        winPosX = self.ReadInt( self._keyWinPosX )
        winPosY = self.ReadInt( self._keyWinPosY )
        winSizeX = self.ReadInt( self._keyWinSizeX )
        winSizeY = self.ReadInt( self._keyWinSizeY )
        
        self.DeleteAll()
        
        if self.win is not None:
            
            # Don't save maximized window properties
            if not self.win.IsMaximized():
                winPosX, winPosY = self.win.GetPosition()
                winSizeX, winSizeY = self.win.GetSize()
            
            # Save the managed window position and size
            self.SavePosition( winPosX, winPosY )
            self.SaveSize( winSizeX, winSizeY )
            
            # Save the managed window state
            winMax = self.win.IsMaximized()
            self.WriteBool( self._keyWinMax, winMax )
        
        # Save the current perspective as the default
        self.Write( self._keyPerspDefault, self.auiMgr.SavePerspective() )
        
    def SavePosition( self, x, y ):
        """Save the managed window's position."""
        self.WriteInt( self._keyWinPosX, x )
        self.WriteInt( self._keyWinPosY, y )
        
    def SaveSize( self, x, y ):
        """Save the managed window's size."""
        self.WriteInt( self._keyWinSizeX, x )
        self.WriteInt( self._keyWinSizeY, y )
    
    def Load( self ):
        """Load all panel layouts for the aui manager."""
        if self.win is not None:
            
            # Load the managed window state
            winMax = self.ReadBool( self._keyWinMax )
            self.win.Maximize( winMax )
            
            # Load the managed window size
            winSizeX = self.ReadInt( self._keyWinSizeX )
            winSizeY = self.ReadInt( self._keyWinSizeY )
            self.win.SetSize( (winSizeX, winSizeY) )
                
            # Load the managed window position
            winPosX = self.ReadInt( self._keyWinPosX )
            winPosY = self.ReadInt( self._keyWinPosY )
            self.win.SetPosition( (winPosX, winPosY) )
            
        # Load the default perspective
        self.auiMgr.LoadPerspective( self.Read( self._keyPerspDefault ) )