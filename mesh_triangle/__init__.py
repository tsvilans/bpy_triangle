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
    "blender": (2, 80, 0),
    "location": "View3D > Toolbar",
    "warning": "",
    "description": "A two-dimensional quality mesh generator and Delaunay triangulator.",
    "wiki_url": "http://www.cs.cmu.edu/~quake/triangle.html"
                "Scripts/Modeling/Triangle",
    "category": "Mesh",
}

import bpy, bmesh,os
from mesh_triangle.triangle import triangulate
from bpy.props import StringProperty, BoolProperty, FloatProperty

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
    mesh_in = obj_in.to_mesh()
    verts = [x.co for x in mesh_in.vertices]
    Nv = len(verts)
    faces = [[y for y in x.vertices] for x in mesh_in.polygons]
    border = get_nonmanifold_edges(mesh_in)

    #if ('v' in args or 'D' in args):
    #    return triangulate(verts, faces, border, args, True)[1]
    res = triangulate(verts, faces, border, args)
    return (res[0], res[1], Nv)

def add_mesh(verts, faces, mesh_name, obj_name):
    bm = bmesh.new()
    for v in verts:
        bm.verts.new(v)
    bm.verts.ensure_lookup_table()

    for f in faces:
        bm.faces.new([bm.verts[x] for x in f])
    bm.faces.ensure_lookup_table()
    bm.verts.index_update()

    m = bpy.data.meshes.new(mesh_name)
    bm.to_mesh(m)
    bm.free()

    o = bpy.data.objects.new(obj_name, m)

    return o

class Triangulate(bpy.types.Operator):
    bl_idname = "object.triangulate"
    bl_label = "Triangulate (Triangle)"
    bl_options = {'REGISTER', 'UNDO'}

    args: StringProperty(
            name="Args",
            description="Input arguments for Triangle",
            default="pq20a1ziV",
            )

    use_args: BoolProperty(
            name="Use args",
            description="Use command line arg string instead of checkboxes",
            default=False)

    cl_p: BoolProperty(
            name="PSLG",
            description="Triangulates a Planar Straight Line Graph (.poly file)",
            default=True)
    cl_r: BoolProperty(
            name="Refine",
            description="Refines a previously generated mesh",
            default=False)
    cl_q: BoolProperty(
            name="Quality",
            description="Quality mesh generation with no angles smaller than the specified angle",
            default=True)
    cl_q_angle: FloatProperty(
            name="Quality angle",
            description="Angle limit for quality mesh generation",
            default=20.0,
            max=35.0,
            min=0.0)
    cl_a: BoolProperty(
            name="Area",
            description="Imposes a maximum triangle area constraint",
            default = False)
    cl_a_value: FloatProperty(
            name="Area value",
            description="Value for area constraint",
            default=1.0,
            min=0.001)
    cl_c: BoolProperty(
            name="Convex hull",
            description="Encloses the convex hull with segments",
            default=False)
    cl_D: BoolProperty(
            name="Delaunay",
            description="Conforming Delaunay: use this switch if you want " \
            "all triangles in the mesh to be Delaunay, and not just constrained " \
            "Delaunay; or if you want to ensure that all Voronoi vertices lie within " \
            "the triangulation",
            default=False)
    cl_v: BoolProperty(
            name="Voronoi",
            description="Outputs the Voronoi diagram associated with the triangulation. "\
            "Does not attempt to detect degeneracies, so some Voronoi vertices may be duplicated",
            default=False)

    def construct_args(self):
        if (self.use_args):
            return self.args
        args = ""
        if self.cl_p: 
            args += 'p'
        if self.cl_r: 
            args += 'r'
        if self.cl_q:
            args+= 'q%f' % self.cl_q_angle
        if self.cl_a:
            args += 'a%f' % self.cl_a_value
        if self.cl_c:
            args += 'c'
        if self.cl_D:
            args += 'D'
        if self.cl_v:
            args += 'v'

        args += 'ziQ'
        return args

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        box = col.box()
        row = box.row(align=True)
        row.prop(self, "use_args", text="Use args")

        if self.use_args:
            row = box.row(align=True)
            row.prop(self, "args", text="Args")

        layout.separator()

        if not self.use_args:

            box = col.box()

            row = box.row(align=True)
            row.prop(self, "cl_q")
            row.prop(self, "cl_q_angle", text="")
            layout.separator()

            row = box.row(align=True)
            row.prop(self, "cl_a")
            row.prop(self, "cl_a_value", text="")
            layout.separator()

            row = box.row(align=True)
            row.prop(self, "cl_c")
            row.prop(self, "cl_p")
            layout.separator()

            #row = col.row(align=True)
            #row.prop(self, "cl_v")
            #row.prop(self, "cl_D")
            #layout.separator()

            row = box.row(align=True)
            row.prop(self, "cl_r")
            layout.separator()


    def execute(self, ctx):
        args = self.construct_args()
        objs = bpy.context.selected_objects
        for o in objs:
            (verts, faces, N) = triangulate_object(o, args)
            obj = add_mesh(verts, faces, o.data.name + '_triangulated', o.name + '_triangulate')


            if obj.type == 'MESH' and len(o.vertex_groups) > 0:
                for vg in o.vertex_groups:
                    obj.vertex_groups.new(name=vg.name)
                for i, v in enumerate(o.data.vertices):
                    for g in v.groups:
                        obj.vertex_groups[g.group].add([i], g.weight, 'ADD')

            original_verts = [x for x in obj.data.vertices[:N]]
            vg = obj.vertex_groups.new(name="Triangle Boundary")
            vg.add(range(N), 1.0, 'ADD')
            for v in original_verts:
                v.select = True

            obj.matrix_world = o.matrix_world
            ctx.scene.collection.objects.link(obj)
            #ctx.scene.objects.link(obj)

        return {'FINISHED'}

class TRIANGLE_PT_Settings(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
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
    bpy.utils.register_class(TRIANGLE_PT_Settings)

def unregister():
    bpy.utils.unregister_class(TRIANGLE_PT_Settings)
    bpy.utils.unregister_class(Triangulate)

if __name__ == "__main__":
    register()
