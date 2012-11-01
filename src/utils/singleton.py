class Singleton( object ):
    
    """Base singleton class."""
    
    def __new__( cls, *args, **kwargs ):
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = object.__new__( cls )
        return cls._the_instance
    
    @classmethod
    def _reset( cls ):
        """Reset the borg"""
        if '_the_instance' in cls.__dict__:
            del cls._the_instance