import math

import pandac.PandaModules as pm


def GetPointsForSquare( x, y, reverse=False ):
    points = []
    
    points.append( (0, 0) )
    points.append( (0, y) )
    points.append( (x, y) )
    points.append( (x, 0) )
    
    # Reverse the order if necessary
    if reverse:
        points.reverse()
        
    return points
    

def GetPointsForSquare2( x, y, reverse=False ):
    points = []
    
    points.append( pm.Point2(0, 0) )
    points.append( pm.Point2(0, y) )
    points.append( pm.Point2(x, y) )
    points.append( pm.Point2(x, 0) )
    
    # Reverse the order if necessary
    if reverse:
        points.reverse()
        
    return points
    

def GetPointsForBox( x, y, z ):
    points = []
    
    for dx in (0, x):
        for p in GetPointsForSquare( y, z, dx ):
            points.append( (dx, p[0], p[1] ) )
                          
    for dy in (0, y):
        for p in GetPointsForSquare( x, z, not dy ):
            points.append( (p[0], dy, p[1] ) )
                          
    for dz in (0, z):
        for p in GetPointsForSquare( x, y, dz ):
            points.append( (p[0], p[1], dz ) )
    
    return points
    

def GetPointsForArc( degrees, numSegs, reverse=False ):
    points = []
    
    radians = math.radians( degrees )
    for i in range( numSegs + 1 ):
        a = radians * i / numSegs
        y = math.sin( a )
        x = math.cos( a )
        
        points.append( (x, y) )
        
    # Reverse the order if necessary
    if reverse:
        points.reverse()
        
    return points
    

def RotatePoint3( p, v1, v2 ):
    v1 = pm.Vec3( v1 )
    v2 = pm.Vec3( v2 )
    v1.normalize()
    v2.normalize()
    cross = v1.cross( v2 )
    cross.normalize()
    if cross.length():
        a = v1.angleDeg( v2 )
        quat = pm.Quat()
        quat.setFromAxisAngle( a, cross )
        p = quat.xform( p )
        
    return p
    

def GetGeomTriangle( v1, v2, v3 ):
    tri = pm.GeomTriangles( pm.Geom.UHDynamic )
    tri.addVertex( v1 )
    tri.addVertex( v2 )
    tri.addVertex( v3 )
    tri.closePrimitive()
    
    return tri
    

class Arc( pm.NodePath ):
    
    """NodePath class representing a wire arc."""
    
    def __init__( self, radius=1.0, numSegs=16, degrees=360, axis=pm.Vec3(1 , 0, 0),
                  thickness=1.0, origin=pm.Point3(0, 0, 0) ):
        
        # Create line segments
        self.ls = pm.LineSegs()
        self.ls.setThickness( thickness )
        
        # Get the points for an arc
        for p in GetPointsForArc( degrees, numSegs ):
            
            # Draw the point rotated around the desired axis
            p = pm.Point3(p[0], p[1], 0) - origin
            p = RotatePoint3( p, pm.Vec3(0, 0, 1), pm.Vec3( axis ) )
            self.ls.drawTo( p * radius )
        
        # Init the node path, wrapping the lines
        node = self.ls.create()
        pm.NodePath.__init__( self, node )
        

def Circle( radius=1.0, numSegs=16, axis=pm.Vec3(1 , 0, 0),
            thickness=1.0, origin=pm.Point3(0, 0, 0) ):
                
    # Create line segments
    ls = pm.LineSegs()
    ls.setThickness( thickness )
    
    # Get the points for an arc
    for p in GetPointsForArc( 360, numSegs ):
        
        # Draw the point rotated around the desired axis
        p = pm.Point3(p[0], p[1], 0) - origin
        p = RotatePoint3( p, pm.Vec3(0, 0, 1), pm.Vec3( axis ) )
        ls.drawTo( p * radius )
        
    return ls.create()
    

def Square( width=1, height=1, axis=pm.Vec3(1, 0, 0), thickness=1.0, origin=pm.Point3(0, 0, 0) ):
    """Return a geom node representing a wire square."""
    # Create line segments
    ls = pm.LineSegs()
    ls.setThickness( thickness )
    
    # Get the points for a square
    points = GetPointsForSquare( width, height )
    points.append( points[0] )
    for p in points:
        
        # Draw the point rotated around the desired axis
        p = pm.Point3(p[0], p[1], 0) - origin
        p = RotatePoint3( p, pm.Vec3(0, 0, 1), axis )
        ls.drawTo( p )
    
    # Return the geom node
    return ls.create()
        

def Cone( radius=1.0, height=1.0, numSegs=16, degrees=360, 
          axis=pm.Vec3(0, 0, 1), origin=pm.Point3(0, 0, 0) ):
    """Return a geom node representing a cone."""
    # Create vetex data format
    gvf = pm.GeomVertexFormat.getV3n3()
    gvd = pm.GeomVertexData( 'vertexData', gvf, pm.Geom.UHStatic )
    
    # Create vetex writers for each type of data we are going to store
    gvwV = pm.GeomVertexWriter( gvd, 'vertex' )
    gvwN = pm.GeomVertexWriter( gvd, 'normal' )
    
    # Get the points for an arc
    points = GetPointsForArc( degrees, numSegs, True )
    for i in range( len( points ) - 1 ):
        
        # Rotate the points around the desired axis
        p1 = pm.Point3(points[i][0], points[i][1], 0) * radius
        p1 = RotatePoint3( p1, pm.Vec3(0, 0, 1), axis ) - origin
        p2 = pm.Point3(points[i + 1][0], points[i + 1][1], 0) * radius
        p2 = RotatePoint3( p2, pm.Vec3(0, 0, 1), axis ) - origin

        cross = ( p2 - axis ).cross( p1 - axis )
        cross.normalize()
        
        gvwV.addData3f( p1 )
        gvwV.addData3f( axis * height - origin )
        gvwV.addData3f( p2 )
        gvwN.addData3f( cross )
        gvwN.addData3f( cross )
        gvwN.addData3f( cross )
        
        # Base
        gvwV.addData3f( p2 )
        gvwV.addData3f( pm.Point3(0, 0, 0) - origin )
        gvwV.addData3f( p1 )
        gvwN.addData3f( -axis )
        gvwN.addData3f( -axis )
        gvwN.addData3f( -axis )
        
    geom = pm.Geom( gvd )
    for i in range( 0, gvwV.getWriteRow(), 3 ):
        
        # Create and add triangle
        geom.addPrimitive( GetGeomTriangle( i, i + 1, i + 2 ) )
    
    # Init the node path, wrapping the box
    geomNode = pm.GeomNode( 'cone' )
    geomNode.addGeom( geom )
    return geomNode
    

class Box( pm.NodePath ):
    
    """NodePath class representing a polygonal box."""
    
    def __init__( self, width=1, depth=1, height=1, origin=pm.Point3(0, 0, 0) ):
        
        # Create vetex data format
        gvf = pm.GeomVertexFormat.getV3n3()
        gvd = pm.GeomVertexData( 'vertexData', gvf, pm.Geom.UHStatic )
        
        # Create vetex writers for each type of data we are going to store
        gvwV = pm.GeomVertexWriter( gvd, 'vertex' )
        gvwN = pm.GeomVertexWriter( gvd, 'normal' )
        
        # Write out all points
        for p in GetPointsForBox( width, depth, height ):
            gvwV.addData3f( pm.Point3( p ) - origin )
        
        # Write out all the normals
        for n in ( (-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1) ):
            for i in range( 4 ):
                gvwN.addData3f( n )
        
        geom = pm.Geom( gvd )
        for i in range( 0, gvwV.getWriteRow(), 4 ):
            
            # Create and add both triangles
            geom.addPrimitive( GetGeomTriangle( i, i + 1, i + 2 ) )
            geom.addPrimitive( GetGeomTriangle( i, i + 2, i + 3 ) )

        # Init the node path, wrapping the box
        geomNode = pm.GeomNode( 'box' )
        geomNode.addGeom( geom )
        pm.NodePath.__init__( self, geomNode )
        
        
class Polygon( pm.NodePath ):
    
    def __init__( self, points, normals=None, texcoords=None, origin=pm.Point3(0, 0, 0) ):
        
        # Create vetex data format
        gvf = pm.GeomVertexFormat.getV3n3t2()
        gvd = pm.GeomVertexData( 'vertexData', gvf, pm.Geom.UHStatic )
        
        # Create vetex writers for each type of data we are going to store
        gvwV = pm.GeomVertexWriter( gvd, 'vertex' )
        gvwN = pm.GeomVertexWriter( gvd, 'normal' )
        gvwT = pm.GeomVertexWriter( gvd, 'texcoord' )
        
        # Write out all points and normals
        for i, point in enumerate( points ):
            p = pm.Point3( point ) - origin
            gvwV.addData3f( p )
            
            # Calculate tex coords if none specified
            if texcoords is None:
                gvwT.addData2f( p.x / 10.0, p.y / 10.0 )
            else:
                gvwT.addData2f( texcoords[i] )
            
            # Calculate normals if none specified
            if normals is None:
                prevPoint = ( points[-1] if i == 0 else points[i-1] )
                nextPoint = ( points[0] if i == len( points ) - 1 else points[i+1] )
                cross = ( nextPoint - point ).cross( prevPoint - point )
                cross.normalize()
                gvwN.addData3f( cross )
            else:
                gvwN.addData3f( normals[i] )
            
        geom = pm.Geom( gvd )
        for i in range( len( points ) - 1 ):
            
            # Create and add both triangles
            geom.addPrimitive( GetGeomTriangle( 0, i, i + 1 ) )
            
        # Init the node path, wrapping the polygon
        geomNode = pm.GeomNode( 'poly' )
        geomNode.addGeom( geom )
        pm.NodePath.__init__( self, geomNode )
        

def Line( start, end, thickness=1.0 ):
    
    """Return a geom node representing a simple line."""
    
    # Create line segments
    ls = pm.LineSegs()
    ls.setThickness( thickness )
    ls.drawTo( pm.Point3( start ) )
    ls.drawTo( pm.Point3( end ) )
    
    # Return the geom node
    return ls.create()


def QuadWireframe( egg ):
    
    def RecursePoly( node, geo ):
            
        if isinstance( node, pm.EggPolygon ):
            
            # Get each vert position
            poss = []
            for vert in node.getVertices():
                pos3 = vert.getPos3()
                pos = pm.Point3( pos3.getX(), pos3.getY(),pos3.getZ() )
                poss.append( pos )
            
            # Build lines
            geo.combineWith( Line( poss[0], poss[1] ) )
            geo.combineWith( Line( poss[1], poss[2] ) )
            geo.combineWith( Line( poss[2], poss[3] ) )
            geo.combineWith( Line( poss[3], poss[0] ) )
        
        # Recurse down hierarchy
        if hasattr( node, 'getChildren' ):
            for child in node.getChildren():
                RecursePoly( child, geo )
                
        return geo
    
    return RecursePoly( egg, pm.GeomNode( 'quadWireframe' ) )