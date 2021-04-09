class Manager:
    def __init__( self ):
        self.undoList = []
        self.redoList = []
        
    def Undo( self ):
        if len( self.undoList ) < 1:
            print('No more undo')
        else:
            actn = self.undoList.pop()
            self.redoList.append( actn )
            actn.Undo()

    def Redo( self ):
        if len( self.redoList ) < 1:
            print('No more redo')
        else:
            actn = self.redoList.pop()
            self.undoList.append( actn )
            actn.Redo()
        
    def ResetUndo( self ):
        while self.undoList:
            actn = self.undoList.pop()
            actn.Destroy()
            
    def ResetRedo( self ):
        while self.redoList:
            actn = self.redoList.pop()
            actn.Destroy()

    def Reset( self ):
        self.ResetUndo()
        self.ResetRedo()

    def Push( self, actn ):
        self.undoList.append( actn )
        self.ResetRedo()