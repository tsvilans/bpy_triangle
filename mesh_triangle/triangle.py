"""
Copyright 2017 Tom Svilans

http://tomsvilans.com

A Python wrapper / Blender add-on for Triangle:

/*  A Two-Dimensional Quality Mesh Generator and Delaunay Triangulator.      */
/*  (triangle.c)                                                             */
/*                                                                           */
/*  Version 1.6                                                              */
/*  July 28, 2005                                                            */
/*                                                                           */
/*  Copyright 1993, 1995, 1997, 1998, 2002, 2005                             */
/*  Jonathan Richard Shewchuk                                                */
/*  2360 Woolsey #H                                                          */
/*  Berkeley, California  94705-1927                                         */
/*  jrs@cs.berkeley.edu                                                      */

Permission is hereby granted, free of charge, to any person obtaining a copy of this 
software and associated documentation files (the "Software"), to deal in the Software 
without restriction, including without limitation the rights to use, copy, modify, merge, 
publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons 
to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
DEALINGS IN THE SOFTWARE.

"""

import sys

import ctypes, os
from ctypes import POINTER, c_double, c_int, c_char_p, c_void_p

def triprint(msg):
    print("Triangle::" + msg)

lib_name = "Triangle.dll"

#triprint("System: {}".format(os.name))

if os.name == "nt":
    lib_name = "Triangle.dll"
elif os.name == "posix":
    lib_name = "libtriangle.so"

lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), lib_name)

#triprint("Lib path: {}".format(lib_path))
lib = ctypes.CDLL(lib_path)

class TriangleIO(ctypes.Structure):

    _fields_ = [('pointlist', POINTER(c_double)),
                ('pointattributelist', POINTER(c_double)),
                ('pointmarkerList', POINTER(c_int)),
                ('numberofpoints', c_int),
                ('numberofpointattributes', c_int),
                ('trianglelist', POINTER(c_int)),
                ('triangleattributelist', POINTER(c_double)),
                ('trianglearealist', POINTER(c_double)),
                ('neighborlist', POINTER(c_int)),
                ('numberoftriangles', c_int),
                ('numberofcorners', c_int),
                ('numberoftriangleattributes', c_int),
                ('segmentlist', POINTER(c_int)),
                ('segmentmarkerlist', POINTER(c_int)),
                ('numberofsegments', c_int),
                ('holelist', POINTER(c_double)),
                ('numberofholes', c_int),
                ('regionlist', POINTER(c_double)),
                ('numberofregions', c_int),
                ('edgelist', POINTER(c_int)),
                ('edgemarkerlist', POINTER(c_int)),
                ('normlist', POINTER(c_double)),
                ('numberofedges', c_int)]

    def __init__(self):
        
        pointlist = 0
        pointattributelist = 0
        pointmarkerList = 0
        numberofpoints = 0
        numberofpointattributes = 0
        trianglelist = 0
        triangleattributelist = 0
        trianglearealist = 0
        neighborlist = 0
        numberoftriangles = 0
        numberofcorners = 0
        numberoftriangleattributes = 0
        segmentlist = 0
        segmentmarkerlist = 0
        numberofsegments = 0
        holelist = 0
        numberofholes = 0
        regionlist = 0
        numberofregions = 0
        edgelist = 0
        edgemarkerlist = 0
        normlist = 0
        numberofedges = 0

lib.triangulate.argtypes = [c_char_p, POINTER(TriangleIO), POINTER(TriangleIO), POINTER(TriangleIO)]
lib.trifree.argtypes = [c_void_p]

def createTriangleIO(verts, faces, segments):
    io = TriangleIO()

    N = len(verts)
    points2d_raw = []
    for i in range(N):
        points2d_raw.extend(verts[i][:2])

    NF = len(faces)
    faces_raw = []
    areas = []
    for i in range(NF):
        areas.append(0.6)
        for j in range(3):
            faces_raw.append(faces[i][j])
#       for j in range(len(faces[i])):
#           faces_raw.append(faces[i][j])

    NS = len(segments)
    segments_raw = []
    for i in range(NS):
        segments_raw.extend(segments[i][:2])

    pointmarkerlist = []
    for i in range(N):
        pointmarkerlist.append(i)


    segmentmarkerlist = []
    for i in range(NS):
        segmentmarkerlist.append(i)

    regionlist = [0.0, 0.0, 0.0, 0.0]

    io.pointlist = (c_double * len(points2d_raw))(*points2d_raw)
    io.pointattributelist = None
    io.pointmarkerList = (c_int * N)(*pointmarkerlist)
    io.numberofpoints = N
    io.numberofpointattributes = 0
    io.trianglelist = (c_int * (NF * 3))(*faces_raw)
    io.triangleattributelist = None
    io.trianglearealist = (c_double * NF)(*areas)
    io.neighborlist = None
    io.numberoftriangles = NF
    io.numberofcorners = 3
    io.numberoftriangleattributes = 0
    io.segmentlist = (c_int * (NS * 2))(*segments_raw)
    io.segmentmarkerlist = (c_int * NS)(*segmentmarkerlist)
    io.numberofsegments = NS

    #holelist = [0.0, 0.0]
    #io.holelist = (c_double * 2)(*holelist)
    #io.numberofholes = 1
    io.holelist = None
    io.numberofholes = 0
    #io.regionlist = (c_double * (1 * 4))(*regionlist)
    #io.numberofregions = 1
    io.regionlist = None
    io.numberofregions = 0
    io.edgelist = None
    io.edgemarkerlist = None
    io.normlist = None
    io.numberofedges = 0    

    return io

def createMesh(tio):
    verts = []
    faces = []

    N = int(tio.numberofpoints)
    ii = 0
    for i in range(N):
        ii = i * 2
        x = float(tio.pointlist[ii])
        y = float(tio.pointlist[ii + 1])
        verts.append((x, y, 0.0))

    NF = int(tio.numberoftriangles)
    triprint ("Number of triangles: %i" % NF)

    for i in range(NF):
        ii = i * 3
        a = int(tio.trianglelist[ii])
        b = int(tio.trianglelist[ii + 1])
        c = int(tio.trianglelist[ii + 2])
        faces.append((a, b, c))

    return (verts, faces)

def triangulate(verts, faces, border, args, vor=False):
    in_mesh = createTriangleIO(verts, faces, border)
    out_mesh = TriangleIO()
    vor_mesh = TriangleIO()

    mutable_string = ctypes.create_string_buffer(str.encode(args))
    res = lib.triangulate(mutable_string, in_mesh, out_mesh, vor_mesh)

    if vor:
        return (createMesh(out_mesh), createMesh(vor_mesh))
    return createMesh(out_mesh)


if __name__ == '__main__':

    print("Start test...")
    #verts = [(0,0,0), (1,0,0), (1,1,0), (0,1,0)]
    #faces = [(0, 1, 2), (1, 2, 3)]
    #segments = [(0,1), (1,2), (2,3), (3,0)]
    #in_mesh = createTriangleIO(verts, faces, segments)
    #out_mesh = TriangleIO()
    #vor_mesh = TriangleIO()

    #res = lib.triangulate("pczAevn".encode('utf-8'), in_mesh, out_mesh, vor_mesh)

    print("Test")

