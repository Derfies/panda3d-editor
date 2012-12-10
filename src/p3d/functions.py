import pandac.PandaModules as pm


def Str2Bool( string ):
    if string.lower() == 'true':
        return True
    return False
        

def FloatTuple2Str( flts ):
    return ' '.join( [str( flt ) for flt in flts] )
    

def Str2FloatTuple( string ):
    buffer = string.split( ' ' )
    return tuple( [float( elem ) for elem in buffer] )
    

def Str2Vec2( string ):
    buffer = string.split( ' ' )
    return pm.Vec2( *[float( buffer[i] ) for i in range( 2 )] )
    

def Str2Vec3( string ):
    buffer = string.split( ' ' )
    return pm.Vec3( *[float( buffer[i] ) for i in range( 3 )] )
    

def Str2Vec4( string ):
    buffer = string.split( ' ' )
    return pm.Vec4( *[float( buffer[i] ) for i in range( 4 )] )
    

def Str2Point2( string ):
    buffer = string.split( ' ' )
    return pm.Point2( *[float( buffer[i] ) for i in range( 2 )] )
    

def Str2Point3( string ):
    buffer = string.split( ' ' )
    return pm.Point3( *[float( buffer[i] ) for i in range( 3 )] )
    

def Str2Point4( string ):
    buffer = string.split( ' ' )
    return pm.Point4( *[float( buffer[i] ) for i in range( 4 )] )
    

def Mat42Str( mat ):
    buffer = [FloatTuple2Str( mat.getRow( i ) ) for i in range( 4 )]
    return ' '.join( buffer )
    

def Str2Mat4( string ):
    mat = pm.Mat4()
    mat.set( *Str2FloatTuple( string ) )
    return mat