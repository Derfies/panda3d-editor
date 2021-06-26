import math

import panda3d.core as pm
import panda3d.core as pc


class VertexDataWriter:

    def __init__(self, vdata):
        self.count = 0
        self.vertex = pc.GeomVertexWriter(vdata, 'vertex')
        self.normal = pc.GeomVertexWriter(vdata, 'normal')
        self.color = pc.GeomVertexWriter(vdata, 'color')
        self.texcoord = pc.GeomVertexWriter(vdata, 'texcoord')

    def add_vertex(self, vertex, normal, color, texcoord):
        self.vertex.add_data3f(vertex)
        self.normal.add_data3f(normal)
        self.color.add_data4f(*color)
        self.texcoord.add_data2f(*texcoord)
        self.count += 1


class Polygon:

    def __init__(self, vertices=None, texcoords=None, colour=None):
        self.vertices = vertices or []
        self.texcoords = texcoords or []
        self.colour = colour or (1, 1, 1, 1)

    def get_normal(self):
        seen = set()
        vertices = [p for p in self.vertices if p not in seen and not seen.add(p)]
        if len(vertices) >= 3:
            v1 = vertices[0] - vertices[1]
            v2 = vertices[1] - vertices[2]
            normal = v1.cross(v2)
            normal.normalize()
        else:
            normal = pc.Vec3.up()
        return normal

    def reverse(self):
        self.vertices.reverse()
        self.texcoords.reverse()


def get_square_points(x, y, reverse=False):
    vertices = [
        (-x / 2.0, -y / 2.0),
        (-x / 2.0, y / 2.0),
        (x / 2.0, y / 2.0),
        (x / 2.0, -y / 2.0),
    ]
    if reverse:
        vertices.reverse()
    return vertices


class InvalidPrimitive(Exception):
    pass


class GeomBuilder:

    def __init__(self, name='tris'):
        self.name = name
        self.vdata = pc.GeomVertexData(
            name,
            pc.GeomVertexFormat.get_v3n3cpt2(),
            pc.Geom.UHDynamic,
        )
        self.writer = VertexDataWriter(self.vdata)
        self.tris = pc.GeomTriangles(pc.Geom.UHDynamic)

    def _commit_polygon(self, poly):
        """
        Transmutes colors and vertices for tris and quads into visible geometry.

        """
        vertex_id = self.writer.count
        for i in range(len(poly.vertices)):
            v, t = poly.vertices[i], poly.texcoords[i]
            self.writer.add_vertex(v, poly.get_normal(), poly.colour, t)

        if len(poly.vertices) == 3:
            self.tris.add_consecutive_vertices(vertex_id, 3)
            self.tris.close_primitive()
        elif len(poly.vertices) == 4:
            self.tris.add_vertex(vertex_id)
            self.tris.add_vertex(vertex_id + 1)
            self.tris.add_vertex(vertex_id + 3)
            self.tris.close_primitive()
            self.tris.add_consecutive_vertices(vertex_id + 1, 3)
            self.tris.close_primitive()
        else:
            raise InvalidPrimitive

    def add_box(self, width, height, depth, colour=None, origin=None, flip_normals=False, scale_texcoords=True):

        origin = origin or pc.Point3(0, 0, 0)
        x_shift = width / 2.0
        y_shift = height / 2.0
        z_shift = depth / 2.0

        vertices = (
            pc.Point3(-x_shift, +y_shift, +z_shift),
            pc.Point3(-x_shift, -y_shift, +z_shift),
            pc.Point3(+x_shift, -y_shift, +z_shift),
            pc.Point3(+x_shift, +y_shift, +z_shift),
            pc.Point3(+x_shift, +y_shift, -z_shift),
            pc.Point3(+x_shift, -y_shift, -z_shift),
            pc.Point3(-x_shift, -y_shift, -z_shift),
            pc.Point3(-x_shift, +y_shift, -z_shift),
        )
        vertices = [v - origin for v in vertices]

        faces = (
            # XY
            [vertices[0], vertices[1], vertices[2], vertices[3]],
            [vertices[4], vertices[5], vertices[6], vertices[7]],
            # XZ
            [vertices[0], vertices[3], vertices[4], vertices[7]],
            [vertices[6], vertices[5], vertices[2], vertices[1]],
            # YZ
            [vertices[5], vertices[4], vertices[3], vertices[2]],
            [vertices[7], vertices[6], vertices[1], vertices[0]],
        )

        # texcoords = ((0, 0), (1, 0), (1, 1), (0, 1))
        face_texcoords = (
            # XY
            ((0, 0), (height, 0), (height, width), (0, width)),
            ((0, 0), (height, 0), (height, width), (0, width)),
            # XZ
            ((0, 0), (width, 0), (width, depth), (0, depth)),
            ((0, 0), (width, 0), (width, depth), (0, depth)),
            # YZ
            ((0, 0), (height, 0), (height, depth), (0, depth)),
            ((0, 0), (height, 0), (height, depth), (0, depth)),
        )

        for i, face in enumerate(faces):
            if flip_normals:
                face.reverse()
            self._commit_polygon(Polygon(face, face_texcoords[i], colour))

        return self

    def get_geom(self):
        geom = pc.Geom(self.vdata)
        geom.add_primitive(self.tris)
        return geom

    def get_geom_node(self):
        node = pc.GeomNode(self.name)
        node.add_geom(self.get_geom())
        return node


def GetPointsForArc(degrees, num_segs, reverse=False):
    points = []
    
    radians = math.radians(degrees)
    for i in range(num_segs + 1):
        a = radians * i / num_segs
        y = math.sin(a)
        x = math.cos(a)
        
        points.append((x, y))
        
    # Reverse the order if necessary
    if reverse:
        points.reverse()
        
    return points
    

def RotatePoint3(p, v1, v2):
    """
    Return the input point rotated around the cross of the input vectors. The
    amount to rotate is the angle between the two vectors.
    """
    v1 = pm.Vec3(v1)
    v2 = pm.Vec3(v2)
    v1.normalize()
    v2.normalize()
    cross = v1.cross(v2)
    cross.normalize()
    if cross.length():
        a = v1.angleDeg(v2)
        quat = pm.Quat()
        quat.setFromAxisAngle(a, cross)
        p = quat.xform(p)
        
    return p
    

def GetGeomTriangle(v1, v2, v3):
    tri = pm.GeomTriangles(pm.Geom.UHDynamic)
    tri.addVertex(v1)
    tri.addVertex(v2)
    tri.addVertex(v3)
    tri.closePrimitive()
    return tri
    

class Arc(pm.NodePath):
    
    """NodePath class representing a wire arc."""
    
    def __init__(self, radius=1.0, numSegs=16, degrees=360, axis=pm.Vec3(1 , 0, 0),
                  thickness=1.0, origin=pm.Point3(0, 0, 0)):
        
        # Create line segments
        self.ls = pm.LineSegs()
        self.ls.setThickness(thickness)
        
        # Get the points for an arc
        for p in GetPointsForArc(degrees, numSegs):
            
            # Draw the point rotated around the desired axis
            p = pm.Point3(p[0], p[1], 0) - origin
            p = RotatePoint3(p, pm.Vec3(0, 0, 1), pm.Vec3(axis))
            self.ls.drawTo(p * radius)
        
        # Init the node path, wrapping the lines
        node = self.ls.create()
        pm.NodePath.__init__(self, node)
        

def Circle(radius=1.0, numSegs=16, axis=pm.Vec3(1 , 0, 0),
            thickness=1.0, origin=pm.Point3(0, 0, 0)):
                
    # Create line segments
    ls = pm.LineSegs()
    ls.setThickness(thickness)
    
    # Get the points for an arc
    for p in GetPointsForArc(360, numSegs):
        
        # Draw the point rotated around the desired axis
        p = pm.Point3(p[0], p[1], 0) - origin
        p = RotatePoint3(p, pm.Vec3(0, 0, 1), pm.Vec3(axis))
        ls.drawTo(p * radius)
        
    return ls.create()
    

def Square(width=1, height=1, axis=pm.Vec3(1, 0, 0), thickness=1.0, origin=pm.Point3(0, 0, 0)):
    """Return a geom node representing a wire square."""
    # Create line segments
    ls = pm.LineSegs()
    ls.setThickness(thickness)
    
    # Get the points for a square
    points = get_square_points(width, height)
    points.append(points[0])
    for p in points:
        
        # Draw the point rotated around the desired axis
        p = pm.Point3(p[0], p[1], 0) - origin
        p = RotatePoint3(p, pm.Vec3(0, 0, 1), axis)
        ls.drawTo(p)
    
    # Return the geom node
    return ls.create()
        

def cone(radius=1.0, height=2.0, num_segs=16, degrees=360,
         axis=pm.Vec3(0, 0, 1), origin=pm.Point3(0, 0, 0)):
    """Return a geom node representing a cone."""
    # Create vetex data format
    gvf = pm.GeomVertexFormat.getV3n3()
    gvd = pm.GeomVertexData('vertexData', gvf, pm.Geom.UHStatic)
    
    # Create vetex writers for each type of data we are going to store
    gvwV = pm.GeomVertexWriter(gvd, 'vertex')
    gvwN = pm.GeomVertexWriter(gvd, 'normal')
    
    # Get the points for an arc
    axis2 = pm.Vec3(axis)
    axis2.normalize()
    offset = axis2 * height / 2.0
    points = GetPointsForArc(degrees, num_segs, True)
    for i in range(len(points) - 1):
        
        # Rotate the points around the desired axis
        p1 = pm.Point3(points[i][0], points[i][1], 0) * radius
        p1 = RotatePoint3(p1, pm.Vec3(0, 0, 1), axis) - origin
        p2 = pm.Point3(points[i + 1][0], points[i + 1][1], 0) * radius
        p2 = RotatePoint3(p2, pm.Vec3(0, 0, 1), axis) - origin

        cross = (p2 - axis).cross(p1 - axis)
        cross.normalize()
        
        # Facet
        gvwV.addData3f(p1 - offset)
        gvwV.addData3f(offset - origin)
        gvwV.addData3f(p2 - offset)
        for i in range(3):
            gvwN.addData3f(cross)
        
        # Base
        gvwV.addData3f(p2 - offset)
        gvwV.addData3f(-offset - origin)
        gvwV.addData3f(p1 - offset)
        for i in range(3):
            gvwN.addData3f(-axis)
        
    geom = pm.Geom(gvd)
    for i in range(0, gvwV.getWriteRow(), 3):
        
        # Create and add triangle
        geom.addPrimitive(GetGeomTriangle(i, i + 1, i + 2))
    
    # Return the cone GeomNode
    geomNode = pm.GeomNode('cone')
    geomNode.addGeom(geom)
    return geomNode
    

def cylinder(radius=1.0, height=2.0, num_segs=16, degrees=360,
             axis=pm.Vec3(0, 0, 1), origin=pm.Point3(0, 0, 0)):
    """Return a geom node representing a cylinder."""
    # Create vetex data format
    gvf = pm.GeomVertexFormat.getV3n3()
    gvd = pm.GeomVertexData('vertexData', gvf, pm.Geom.UHStatic)
    
    # Create vetex writers for each type of data we are going to store
    gvwV = pm.GeomVertexWriter(gvd, 'vertex')
    gvwN = pm.GeomVertexWriter(gvd, 'normal')
    
    # Get the points for an arc
    #offset = height / 2.0
    axis2 = pm.Vec3(axis)
    axis2.normalize()
    offset = axis2 * height / 2.0
    points = GetPointsForArc(degrees, num_segs, True)
    for i in range(len(points) - 1):
        
        # Rotate the points around the desired axis
        p1 = pm.Point3(points[i][0], points[i][1], 0) * radius
        p1 = RotatePoint3(p1, pm.Vec3(0, 0, 1), axis) - origin
        p2 = pm.Point3(points[i + 1][0], points[i + 1][1], 0) * radius
        p2 = RotatePoint3(p2, pm.Vec3(0, 0, 1), axis) - origin

        # Base
        gvwV.addData3f(p2 - offset)
        gvwV.addData3f(-offset - origin)
        gvwV.addData3f(p1 -offset)
        for i in range(3):
            gvwN.addData3f(-axis)
        
        # Cap
        gvwV.addData3f(p1 + offset)
        gvwV.addData3f(offset - origin)
        gvwV.addData3f(p2 + offset)
        for i in range(3):
            gvwN.addData3f(axis)
        
        # Sides
        gvwV.addData3f(p1 + offset)
        gvwV.addData3f(p2 + offset)
        gvwV.addData3f(p1 - offset)
        gvwV.addData3f(p2 - offset)
        gvwV.addData3f(p1 - offset)
        gvwV.addData3f(p2 + offset)
        cross = (p1 + offset - p1).cross(p2 - p1)
        for i in range(6):
            gvwN.addData3f(cross)
        
    geom = pm.Geom(gvd)
    for i in range(0, gvwV.getWriteRow(), 3):
        
        # Create and add triangle
        geom.addPrimitive(GetGeomTriangle(i, i + 1, i + 2))
    
    # Return the cylinder GeomNode
    geomNode = pm.GeomNode('cylinder')
    geomNode.addGeom(geom)
    return geomNode
    

def sphere(radius=1.0, num_segs=16, degrees=360,
           axis=pm.Vec3(0, 0, 1), origin=pm.Point3(0, 0, 0)):
    """Return a geom node representing a cylinder."""
    # Create vetex data format
    gvf = pm.GeomVertexFormat.getV3n3()
    gvd = pm.GeomVertexData('vertexData', gvf, pm.Geom.UHStatic)

    # Create vetex writers for each type of data we are going to store
    gvwV = pm.GeomVertexWriter(gvd, 'vertex')
    gvwN = pm.GeomVertexWriter(gvd, 'normal')

    # Get the points for an arc
    axis = pm.Vec3(axis)
    axis.normalize()
    points = GetPointsForArc(degrees, num_segs, True)
    zPoints = GetPointsForArc(180, int(num_segs / 2), True)
    for z in range(1, len(zPoints) - 2):
        rad1 = zPoints[z][1] * radius
        rad2 = zPoints[z+1][1] * radius
        offset1 = axis * zPoints[z][0] * radius
        offset2 = axis * zPoints[z+1][0] * radius
        
        for i in range(len(points) - 1):
            
            # Get points
            p1 = pm.Point3(points[i][0], points[i][1], 0) * rad1
            p2 = pm.Point3(points[i + 1][0], points[i + 1][1], 0) * rad1
            p3 = pm.Point3(points[i + 1][0], points[i + 1][1], 0) * rad2
            p4 = pm.Point3(points[i][0], points[i][1], 0) * rad2
            
            # Rotate the points around the desired axis
            p1, p2, p3, p4 = [
                RotatePoint3(p, pm.Vec3(0, 0, 1), axis) 
                for p in [p1, p2, p3, p4]
            ]
            
            a = p1 + offset1 - origin
            b = p2 + offset1 - origin
            c = p3 + offset2 - origin
            d = p4 + offset2 - origin

            # Quad
            gvwV.addData3f(d)
            gvwV.addData3f(b)
            gvwV.addData3f(a)
            gvwV.addData3f(d)
            gvwV.addData3f(c)
            gvwV.addData3f(b)
            
            # Normals
            cross = (b - c).cross(a - c)
            for i in range(6):
                gvwN.addData3f(cross)
                
    # Get points
    rad1 = zPoints[1][1] * radius
    for m in [1, -2]:
        offset1 = axis * zPoints[m][0] * radius
        
        clampedM = max(-1, min(m, 1)) * radius
        
        for i in range(len(points) - 1):
            p1 = pm.Point3(points[i][0], points[i][1], 0) * rad1
            p2 = pm.Point3(points[i + 1][0], points[i + 1][1], 0) * rad1
            
            # Rotate the points around the desired axis
            p1, p2 = [
                RotatePoint3(p, pm.Vec3(0, 0, 1), axis) 
                for p in [p1, p2]
            ]
            
            a = p1 + offset1 - origin
            b = p2 + offset1 - origin
            c = -axis * clampedM

            # Quad
            if clampedM > 0:
                gvwV.addData3f(a)
                gvwV.addData3f(b)
                gvwV.addData3f(c)
            else:
                gvwV.addData3f(c)
                gvwV.addData3f(b)
                gvwV.addData3f(a)
            
            # Normals
            cross = (b - c).cross(a - c)
            for i in range(3):
                gvwN.addData3f(cross * -m)

    geom = pm.Geom(gvd)
    for i in range(0, gvwV.getWriteRow(), 3):

        # Create and add triangle
        geom.addPrimitive(GetGeomTriangle(i, i + 1, i + 2))

    # Return the cylinder GeomNode
    geomNode = pm.GeomNode('cylinder')
    geomNode.addGeom(geom)
    return geomNode
    

def box(width=1, depth=1, height=1, origin=pm.Point3(0, 0, 0), flip_normals=False, scale_texcoords=True):
    """Return a geom node representing a box."""
    gb = GeomBuilder('box')
    gb.add_box(width, depth, height, origin=origin, flip_normals=flip_normals, scale_texcoords=scale_texcoords)
    return gb.get_geom_node()


def Line(start, end, thickness=1.0):
    """Return a geom node representing a simple line."""
    # Create line segments
    ls = pm.LineSegs()
    ls.setThickness(thickness)
    ls.drawTo(pm.Point3(start))
    ls.drawTo(pm.Point3(end))
    
    # Return the geom node
    return ls.create()


def QuadWireframe(egg):
    
    def RecursePoly(node, geo):
            
        if isinstance(node, pm.EggPolygon):
            
            # Get each vert position
            poss = []
            for vert in node.getVertices():
                pos3 = vert.getPos3()
                pos = pm.Point3(pos3.getX(), pos3.getY(),pos3.getZ())
                poss.append(pos)
            
            # Build lines
            geo.combineWith(Line(poss[0], poss[1]))
            geo.combineWith(Line(poss[1], poss[2]))
            geo.combineWith(Line(poss[2], poss[3]))
            geo.combineWith(Line(poss[3], poss[0]))
        
        # Recurse down hierarchy
        if hasattr(node, 'getChildren'):
            for child in node.getChildren():
                RecursePoly(child, geo)
                
        return geo
    
    return RecursePoly(egg, pm.GeomNode('quadWireframe'))
    

def Axes(thickness=1, length=25):
    """Class representing the viewport camera axes."""
    # Build line segments
    ls = pm.LineSegs()
    ls.setThickness(thickness)
    
    # X Axis - Red
    ls.setColor(1.0, 0.0, 0.0, 1.0)
    ls.moveTo(0.0, 0.0, 0.0)
    ls.drawTo(length, 0.0, 0.0)
    
    # Y Axis - Green
    ls.setColor(0.0, 1.0, 0.0, 1.0)
    ls.moveTo(0.0,0.0,0.0)
    ls.drawTo(0.0, length, 0.0)
    
    # Z Axis - Blue
    ls.setColor(0.0, 0.0, 1.0, 1.0)
    ls.moveTo(0.0,0.0,0.0)
    ls.drawTo(0.0, 0.0, length)
    
    return ls.create()
