from direct.showbase.DirectObject import DirectObject


class Object(DirectObject):
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        
        # Default camera to base camera if None is specified
        self.camera = kwargs.pop( 'camera', base.camera )

        # Default root node to render if None is specified
        self.rootNp = kwargs.pop( 'rootNp', render )

        # Default root 2d node to render2d if None is specified
        self.root2d = kwargs.pop( 'root2d', render2d )

        # Default root aspect 2d node to aspect2d if None is specified
        self.rootA2d = kwargs.pop( 'rootA2d', aspect2d )

        # Default root pixel 2d node to pixel2d if None is specified
        self.rootP2d = kwargs.pop( 'rootP2d', pixel2d )

        # Default win to base.win if None specified.
        self.win = kwargs.pop( 'win', base.win )

        # Default mouse watcher node to base.win if None specified.
        self.mouseWatcherNode = kwargs.pop( 'mouseWatcherNode',
                                            base.mouseWatcherNode )

