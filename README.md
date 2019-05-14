# bpy_triangle
A Blender add-on for Triangle.
![Triangle in Blender.](https://raw.githubusercontent.com/tsvilans/bpy_triangle/master/triangle.png)

```
Triangle: A Two-Dimensional Quality Mesh Generator and Delaunay Triangulator
Copyright 1993, 1995, 1997, 1998, 2002, 2005
Jonathan Richard Shewchuk
2360 Woolsey #H
Berkeley, California  94705-1927
jrs@cs.berkeley.edu
```

http://www.cs.cmu.edu/~quake/triangle.html

This is a Python wrapper for the Triangle library referenced above. It uses ctypes.
The add-on adds a 'Triangulate' operator to Blender, which can take any planar meshable object 
(curves and meshes) and create a triangulated mesh based on specified input parameters.

Input parameters are provided via a text field and are described in the Triangle documentation.

![Triangle in Blender.](https://raw.githubusercontent.com/tsvilans/bpy_triangle/master/triangle_ui.png)

Further work could be done to expand functionality and add support for meshing Ngon faces or some 
other way of operating out of the XY plane, but for now it is limited to this.

This is especially useful for creating meshes for sculpting or meshes with good face densities
from 2d CAD data, for arch. viz or other uses. Interior edges are respected, meaning creating
dense meshes with interior regions is possible. Note the interior circle in the image above.

# Update 190514

- Added Linux support.
- Compiled updated Triangle lib which fixes issues for newer Windows versions https://github.com/libigl/triangle

# Update 171208

- Added UI with props for the most common / useful flags and settings.
- Added vertex group support: triangulated objects have vertex group (Triangle Boundary) which contains the vertices of the input mesh. This makes it easy to define Softbody / Cloth goals, or anchors, or isolate regions. Bear in mind, if input edges are split, the new vertices won't be added to this vertex group. This might be fixed in the future.

# To do

- ~~Linux: Compile Triangle for Linux and adjust the script if necessary.~~
- Find shortest path between ends of split edges, add the new vertices along that path to the Boundary vertex group.
- Find way to expose holes and regions in Blender UI.

# Contact

tsvi@kadk.dk

http://tomsvilans.com
