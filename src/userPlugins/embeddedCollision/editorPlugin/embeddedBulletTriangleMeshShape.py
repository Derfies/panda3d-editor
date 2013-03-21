from .. import gamePlugin as gp


class EmbeddedBulletTriangleMeshShape( gp.EmbeddedBulletTriangleMeshShape ):
    
    @classmethod
    def Create( cls, *args, **kwargs ):
        from editor.nodes.constants import TAG_MODIFIED
        wrpr = super( EmbeddedBulletTriangleMeshShape, cls ).Create( *args, **kwargs )
        wrpr.data.setPythonTag( TAG_MODIFIED, True )
        return wrpr