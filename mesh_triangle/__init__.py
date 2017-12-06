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


bl_info = {
    "name": "Triangle",
    "author": "Tom Svilans (Blender wrapper)",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Toolbar",
    "warning": "",
    "description": "A two-dimensional quality mesh generator and Delaunay triangulator.",
    "wiki_url": "http://www.cs.cmu.edu/~quake/triangle.html"
                "Scripts/Modeling/Triangle",
    "category": "Mesh",
}

import bpy, bmesh,os
from mesh_triangle.triangle import triangulate
from bpy.props import StringProperty

def get_nonmanifold_edges(mymesh):
    culprits=[]
    for e in mymesh.edges:
            shared = 0
            for f in mymesh.polygons:
                    for vf1 in f.vertices:
                            if vf1 == e.vertices[0]:
                                    for vf2 in f.vertices:
                                            if vf2 == e.vertices[1]:
                                                    shared = shared + 1
            if (shared > 2):
                    culprits.append((e.vertices[0], e.vertices[1]))
            if (shared < 2):
                    culprits.append((e.vertices[0], e.vertices[1]))
    return culprits

def triangulate_object(obj_in, args):
    mesh_in = obj_in.to_mesh(bpy.context.scene, True, 'RENDER')
    verts = [x.co for x in mesh_in.vertices]
    faces = [[y for y in x.vertices] for x in mesh_in.polygons]
    border = get_nonmanifold_edges(mesh_in)

    res = triangulate(verts, faces, border, args)

    bm = bmesh.new()
    
    for i in res[0]:
        v = (i[0], i[1], 0.0)
        bm.verts.new(v)
        
    bm.verts.ensure_lookup_table()

    for i in res[1]:
            bm.faces.new([bm.verts[x] for x in i])
            
    bm.faces.ensure_lookup_table()
    bm.verts.index_update()
    
    mesh_out = bpy.data.meshes.new(mesh_in.name + "_triangulated")

    bm.to_mesh(mesh_out)
    bm.free()
    
    obj_out = bpy.data.objects.new(obj_in.name + "_triangulated", mesh_out)
    obj_out.matrix_world = obj_in.matrix_world
    
    bpy.context.scene.objects.link(obj_out)

class Triangulate(bpy.types.Operator):
    bl_idname = "object.triangulate"
    bl_label = "Triangulate using Triangle"
    bl_options = {'REGISTER', 'UNDO'}

    args = StringProperty(
            name="Args",
            description="Input arguments for Triangle",
            default="pq20a1ziV",
            )

    def execute(self, context):
        objs = bpy.context.selected_objects
        for o in objs:
            triangulate_object(o, self.args)
        return {'FINISHED'}

class TrianglePanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Tools'
    bl_context = "objectmode"
    bl_label = "Triangle"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row = layout.row()
        row.operator("object.triangulate", text='Triangulate')


def menu_func(self, context):
    self.layout.operator(Triangulate.bl_idname, icon='MESH_CUBE')

def register():
    bpy.utils.register_class(Triangulate)
    bpy.utils.register_class(TrianglePanel)

def unregister():
    bpy.utils.unregister_class(Triangulate)
    bpy.utils.unregister_class(TrianglePanel)

if __name__ == "__main__":
    register()
