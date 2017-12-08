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

import ctypes, os
from ctypes import POINTER, c_double, c_int, c_char

dll_path = os.path.dirname(os.path.abspath(__file__)) + '\Triangle.dll'
dll = ctypes.CDLL(dll_path)

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

dll.triangulate.argtypes = [POINTER(c_char), POINTER(TriangleIO), POINTER(TriangleIO), POINTER(TriangleIO)]

def createTriangleIO(verts, faces, segments):
	io = TriangleIO()

	N = len(verts)
	points2d_raw = []
	for i in range(N):
		points2d_raw.append(verts[i][0])
		points2d_raw.append(verts[i][1])

	NF = len(faces)
	faces_raw = []
	for i in range(NF):
		for j in range(len(faces[i])):
			faces_raw.append(faces[i][j])

	NS = len(segments)
	segments_raw = []
	for i in range(NS):
		segments_raw.append(segments[i][0])
		segments_raw.append(segments[i][1])

	pointmarkerlist = []
	for i in range(N):
		pointmarkerlist.append(0)

	segmentmarkerlist = []
	for i in range(NS):
		segmentmarkerlist.append(0)

	regionlist = [0.0, 0.0, 0.0, 0.0]

	io.pointlist = (c_double * (N * 2))(*points2d_raw)
	io.pointattributelist = None
	io.pointmarkerList = (c_int * N)(*pointmarkerlist)
	io.numberofpoints = N
	io.numberofpointattributes = 0
	io.trianglelist = (c_int * (NF * 3))(*faces_raw)
	io.triangleattributelist = None
	io.trianglearealist = None
	io.neighborlist = None
	io.numberoftriangles = NF
	io.numberofcorners = 3
	io.numberoftriangleattributes = 0
	io.segmentlist = (c_int * (NS * 2))(*segments_raw)
	io.segmentmarkerlist = (c_int * NS)(*segmentmarkerlist)
	io.numberofsegments = NS
	io.holelist = None
	io.numberofholes = 0
	io.regionlist = (c_double * (1 * 4))(*regionlist)
	io.numberofregions = 1
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
	print ("Number of triangles: %i" % NF)

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

	res = dll.triangulate(args.encode('utf-8'), ctypes.byref(in_mesh), ctypes.byref(out_mesh), ctypes.byref(vor_mesh))
	if vor:
		return (createMesh(out_mesh), createMesh(vor_mesh))
	return createMesh(out_mesh)

if __name__ == '__main__':
	verts = [(0,0,0), (1,0,0), (1,1,0), (0,1,0)]
	faces = [(0, 1, 2), (1, 2, 3)]
	in_mesh = createTriangleIO(verts, faces)
	out_mesh = TriangleIO()
	vor_mesh = TriangleIO()

	res = dll.triangulate("pczAevn".encode('utf-8'), ctypes.byref(in_mesh), ctypes.byref(out_mesh), ctypes.byref(vor_mesh))

	print(res)

