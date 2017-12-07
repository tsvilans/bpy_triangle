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

# To do

- Linux: Compile Triangle for Linux and adjust the script if necessary.
- UI: Create interface for command line args for Triangle, instead of arg string.

# Contact

tsvi@kadk.dk

http://tomsvilans.com
