class Base:
    
    def __call__(self):
        self.redo()
    
    def undo(self):
        pass
    
    def redo(self):
        pass
    
    def destroy(self):
        pass
