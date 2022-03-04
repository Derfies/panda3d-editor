import math

import panda3d.core as pm
import panda3d.core as pc


def calculate_box_polygons(width, height, depth, colour=None, origin=None, flip_normals=False, scale_texcoords=True):
    origin = origin or pc.Point3(0, 0, 0)
    x_shift = width / 2.0
    y_shift = height / 2.0
    z_shift = depth / 2.0

    positions = (
        pc.Point3(-x_shift, +y_shift, +z_shift),
        pc.Point3(-x_shift, -y_shift, +z_shift),
        pc.Point3(+x_shift, -y_shift, +z_shift),
        pc.Point3(+x_shift, +y_shift, +z_shift),
        pc.Point3(+x_shift, +y_shift, -z_shift),
        pc.Point3(+x_shift, -y_shift, -z_shift),
        pc.Point3(-x_shift, -y_shift, -z_shift),
        pc.Point3(-x_shift, +y_shift, -z_shift),
    )
    positions = [v - origin for v in positions]

    faces = (
        # XY
        [positions[0], positions[1], positions[2], positions[3]],
        [positions[4], positions[5], positions[6], positions[7]],
        # XZ
        [positions[0], positions[3], positions[4], positions[7]],
        [positions[6], positions[5], positions[2], positions[1]],
        # YZ
        [positions[5], positions[4], positions[3], positions[2]],
        [positions[7], positions[6], positions[1], positions[0]],
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

    polygons = []
    for i, face in enumerate(faces):
        if flip_normals:
            face.reverse()
        vertices = [
            Vertex(face[j], texcoord=face_texcoords[i][j])
            for j in range(len(face))
        ]
        polygons.append(Polygon(vertices))

    return polygons


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


class Vertex:

    def __init__(self, position, normal=None, colour=None, texcoord=None):
        self.position = position
        self.normal = normal
        self.colour = colour
        self.texcoord = texcoord


class Polygon:

    def __init__(self, vertices, normal=None):
        self.vertices = vertices
        self._normal = normal

    @property
    def normal(self):
        if self._normal is None:
            seen = set()
            positions = [
                vertex.position
                for vertex in self.vertices
                if vertex.position not in seen and not seen.add(vertex.position)
            ]
            if len(positions) >= 3:
                v1 = positions[0] - positions[1]
                v2 = positions[1] - positions[2]
                normal = v1.cross(v2)
                normal.normalize()
            else:
                normal = pc.Vec3.up()
            self._normal = normal
        return self._normal


class InvalidPrimitive(Exception):
    pass


class VertexDataWriter:

    def __init__(self, name, normal=False, colour=False, texcoord=False):
        self.count = 0
        method_name = 'get_v3'
        if normal:
            method_name += 'n3'
        if colour:
            method_name += 'c4'
        if texcoord:
            method_name += 't2'
        vformat = getattr(pc.GeomVertexFormat, method_name)()
        self.vdata = pc.GeomVertexData(name, vformat, pc.Geom.UHStatic)
        self.position = pc.GeomVertexWriter(self.vdata, 'vertex')
        self.normal = pc.GeomVertexWriter(self.vdata, 'normal') if normal else None
        self.colour = pc.GeomVertexWriter(self.vdata, 'color') if colour else None
        self.texcoord = pc.GeomVertexWriter(self.vdata, 'texcoord') if texcoord else None

    def add_polygon(self, polygon):
        for vertex in polygon.vertices:
            self.position.add_data3f(vertex.position)
            if self.normal is not None:
                self.normal.add_data3f(vertex.normal or polygon.normal)
            if self.colour is not None:
                self.colour.add_data4f(vertex.colour or (1, 1, 1, 1))
            if self.texcoord is not None:
                self.texcoord.add_data2f(vertex.texcoord)
            self.count += 1


class GeomBuilder:

    def __init__(self, polygons=None):
        self.polygons = polygons or []

    def create_geom_node(self, name, **kwargs):
        writer = VertexDataWriter(name, **kwargs)
        tris = pc.GeomTriangles(pc.Geom.UHStatic)
        for polygon in self.polygons:

            # Add geometry data.
            vertex_id = writer.count
            writer.add_polygon(polygon)

            # Define triangles.
            if len(polygon.vertices) == 3:
                tris.add_consecutive_vertices(vertex_id, 3)
                tris.close_primitive()
            elif len(polygon.vertices) == 4:
                tris.add_vertex(vertex_id)
                tris.add_vertex(vertex_id + 1)
                tris.add_vertex(vertex_id + 3)
                tris.close_primitive()
                tris.add_consecutive_vertices(vertex_id + 1, 3)
                tris.close_primitive()
            else:

                # Use triangulator for ngons.
                trig = pm.Triangulator3()
                for vertex in polygon.vertices:
                    vi = trig.addVertex(*vertex.position)
                    trig.addPolygonVertex(vi)
                trig.triangulate()
                for i in range(trig.getNumTriangles()):
                    tris.addVertices(
                        trig.getTriangleV0(i),
                        trig.getTriangleV1(i),
                        trig.getTriangleV2(i),
                    )
                    tris.closePrimitive()

        geom = pc.Geom(writer.vdata)
        geom.add_primitive(tris)
        node = pc.GeomNode(name)
        node.add_geom(geom)
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


def box(width=1, depth=1, height=1, origin=pm.Point3(0, 0, 0), flip_normals=False, scale_texcoords=True, normal=True, colour=False, texcoord=False):
    """Return a geom node representing a box."""
    polys = calculate_box_polygons(
        width,
        depth,
        height,
        origin=origin,
        flip_normals=flip_normals,
        scale_texcoords=scale_texcoords
    )
    return GeomBuilder(polys).create_geom_node('box', normal=normal, colour=colour, texcoord=texcoord)


def sphere(radius=1.0, num_segs=16, degrees=360, axis=pm.Vec3(0, 0, 1), origin=pm.Point3(0, 0, 0), normal=True, colour=False, texcoord=False):
    """Return a geom node representing a cylinder."""
    polys = []

    # Get the points for an arc
    axis = pm.Vec3(axis)
    axis.normalize()
    points = GetPointsForArc(degrees, num_segs, True)
    zPoints = GetPointsForArc(180, int(num_segs / 2), True)
    for z in range(1, len(zPoints) - 2):
        rad1 = zPoints[z][1] * radius
        rad2 = zPoints[z + 1][1] * radius
        offset1 = axis * zPoints[z][0] * radius
        offset2 = axis * zPoints[z + 1][0] * radius

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

            polys.append(Polygon((
                Vertex(d),
                Vertex(c),
                Vertex(b),
                Vertex(a),
            )))

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
                polys.append(Polygon((
                    Vertex(a),
                    Vertex(b),
                    Vertex(c),
                )))
            else:
                polys.append(Polygon((
                    Vertex(c),
                    Vertex(b),
                    Vertex(a),
                )))

    return GeomBuilder(polys).create_geom_node('sphere', normal=normal, colour=colour, texcoord=texcoord)


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
