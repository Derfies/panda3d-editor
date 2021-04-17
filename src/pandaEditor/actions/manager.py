import logging


logger = logging.getLogger(__name__)


class Manager:

    def __init__(self):
        self.undoList = []
        self.redoList = []
        
    def Undo(self):
        if len(self.undoList) < 1:
            logger.info('No more undo')
        else:
            actn = self.undoList.pop()
            self.redoList.append(actn)
            actn.undo()

    def Redo(self):
        if len(self.redoList) < 1:
            logger.info('No more redo')
        else:
            actn = self.redoList.pop()
            self.undoList.append(actn)
            actn.redo()
        
    def ResetUndo(self):
        while self.undoList:
            actn = self.undoList.pop()
            actn.destroy()
            
    def ResetRedo(self):
        while self.redoList:
            actn = self.redoList.pop()
            actn.destroy()

    def Reset(self):
        self.ResetUndo()
        self.ResetRedo()

    def Push(self, actn):
        self.undoList.append(actn)
        self.ResetRedo()
