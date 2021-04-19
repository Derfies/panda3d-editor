import abc


class Base(metaclass=abc.ABCMeta):
    
    def __call__(self):
        self.redo()

    @abc.abstractmethod
    def undo(self):
        """"""

    @abc.abstractmethod
    def redo(self):
        """"""
    
    def destroy(self):
        pass
