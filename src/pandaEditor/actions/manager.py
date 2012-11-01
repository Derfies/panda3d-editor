class Manager:
    def __init__( self ):
        self.undoList = []
        self.redoList = []

    def Reset( self ):
        while self.undoList:
            actn = self.undoList.pop()
            actn.Destroy()

        while self.redoList:
            actn = self.redoList.pop()
            actn.Destroy()

    def Push( self, actn ):
        #print 'PUSH: ', actn
        self.undoList.append( actn )
        #if self.redoList:
        #    self.redoList.pop()
        while self.redoList:
            actn = self.redoList.pop()
            actn.Destroy()

    def Undo( self ):
        if len( self.undoList ) < 1:
            print 'No more undo'
        else:
            actn = self.undoList.pop()
            self.redoList.append( actn )
            actn.Undo()
            #print 'UNDO: ', actn

    def Redo( self ):
        if len( self.redoList ) < 1:
            print 'No more redo'
        else:
            actn = self.redoList.pop()
            self.undoList.append( actn )
            actn.Redo()
            #print 'REDO: ', actn