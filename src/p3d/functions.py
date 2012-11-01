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
    

def Mat42Str( mat ):
    buffer = [FloatTuple2Str( mat.getRow( i ) ) for i in range( 4 )]
    return ' '.join( buffer )
    

def Str2Mat4( string ):
    mat = pm.Mat4()
    mat.set( *Str2FloatTuple( string ) )
    return mat