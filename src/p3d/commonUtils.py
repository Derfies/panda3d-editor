import pandac.PandaModules as pm

import os


def Relpath( target, base=os.curdir ):
    """
    Return a relative path to the target from either the current directory or
    an optional base directory. Base can be a directory specified either as
    absolute or relative to current directory.
    """
    base_list = ( os.path.abspath( base ) ).split( os.sep )
    target_list = (os.path.abspath( target ) ).split( os.sep )
    
    # If the base was just a drive sometimes we get an empty string at the end
    # of the list which messes up the join operation at the end.
    if not base_list[-1]:
        base_list = base_list[:-1]
        
    # On the windows platform the target may be on a completely different
    # drive from the base
    if os.name in ['nt','dos','os2'] and base_list[0].lower() <> target_list[0].lower():
        raise OSError, ''.join( ['Target is on a different drive to base. Target: ', target_list[0], ', base: ', base_list[0]] )

    # Starting from the filepath root, work out how much of the filepath is
    # shared by base and target
    for i in range( min( len( base_list ), len( target_list ) ) ):
        if base_list[i].lower() <> target_list[i].lower(): 
            break
    else:
        
        # If we broke out of the loop, i is pointing to the first differing
        # path elements. If we didn't break out of the loop, i is pointing to
        # identical path elements. Increment i so that in all cases it points
        # to the first differing path elements.
        i += 1
        
    rel_list = [os.pardir] * ( len( base_list ) - i ) + target_list[i:]
    return os.path.join( *rel_list )
    

def GetTrsMatrices( xform ):
    """
    Return translation, rotation and scale matrices back for the specified
    transform.
    """
    # Get translation and rotation matrices
    rotMat = pm.Mat4()
    xform.getQuat().extractToMatrix( rotMat )
    transMat = pm.Mat4().translateMat( xform.getPos() )
    
    # More care must be taken to get the scale matrix as simply calling
    # Mat4().scaleMat( xform.getScale() ) won't account for shearing or other
    # weird scaling. To get this matrix simply remove the translation and
    # rotation components from the xform.
    invRotMat = pm.Mat4()
    invRotMat.invertFrom( rotMat )
    invTransMat = pm.Mat4()
    invTransMat.invertFrom( transMat )
    scaleMat = xform.getMat() * invTransMat * invRotMat
    
    return transMat, rotMat, scaleMat
    

def GetInvertedMatrix( mat ):
    """
    Invert the indicated matrix, sending back a new matrix.
    """
    invMat = pm.Mat4()
    invMat.invertFrom( mat )
    return invMat