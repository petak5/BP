import bpy
from bpy.props import FloatProperty
import bmesh
import mathutils
import random

from .erosions import erosion


class CreateTerrainOperator(bpy.types.Operator):
    bl_label = "Create Terrain"
    bl_idname = "object.create_terrain_operator"

    def execute(self, context):
        self.create_terrain(context)
        return {'FINISHED'}

    def create_terrain(self, context):
        new_mesh = bpy.data.meshes.new("MyMesh")
        new_obj = bpy.data.objects.new("NewObject", new_mesh)
        new_collection = bpy.data.collections.new("NewCollection")

        bpy.context.scene.collection.children.link(new_collection)
        new_collection.objects.link(new_obj)

        vertices = []
        polygons = []

        bump_intensity = 1
        grid_size = 200
        step_size = 0.05

        for i in range(0, grid_size, 1):
            for j in range(0, grid_size, 1):
                v = mathutils.Vector((i/10.1, j/10.1, 0.0))
                x = mathutils.noise.fractal(v, 0.4, 1.0, 1)
                vertices.append([i * step_size, j * step_size, x * bump_intensity])

                if i > 0 and j > 0:
                    offset = (i * grid_size) + j
                    # print(f"i = {i}, j = {j}, offset = {offset}")
                    polygons.append([offset - grid_size - 1, offset - 1, offset - grid_size])
                    polygons.append([offset - 1, offset - grid_size, offset])

        new_obj.my_obj_props.old_displacement = bump_intensity

        new_mesh.from_pydata(vertices, [], polygons)


class UpdateTerrainOperator(bpy.types.Operator):
    bl_label = "Update Terrain"
    bl_idname = "object.update_terrain_operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        self.update_terrain(context)
        return {'FINISHED'}

    def update_terrain(self, context):
        active_obj = context.active_object
        active_mesh = active_obj.data
        my_bmesh = bmesh.new()
        my_bmesh.from_mesh(active_mesh)

        obj_properties = active_obj.my_obj_props

        for v in my_bmesh.verts:
            v.co.z *= obj_properties.displacement / obj_properties.old_displacement

        obj_properties.old_displacement = obj_properties.displacement

        my_bmesh.to_mesh(active_mesh)
        my_bmesh.free()


class AnimateObjectOperator(bpy.types.Operator):
    bl_label = "Animate Object"
    bl_idname = "object.animate_object_operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        self.animate_object(context)
        return {'FINISHED'}

    def animate_object(self, context):
        active_obj = context.active_object
        scene = context.scene

        for i in range(20):
            scene.frame_set(i * 3)
            active_obj.location = (0, i, 0)
            active_obj.keyframe_insert("location")


class WiggleObjectOperator(bpy.types.Operator):
    bl_label = "Wiggle Object"
    bl_idname = "object.wiggle_object_operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        self.wiggle_object(context)
        return {'FINISHED'}

    def wiggle_object(self, context):

        active_obj = context.active_object
        active_mesh = active_obj.data
        my_bmesh = bmesh.new()
        my_bmesh.from_mesh(active_mesh)

        for v in my_bmesh.verts:
            delta = random.random() % 0.05
            if random.random() > 0.5:
                delta = -delta
            v.co.z += delta

        my_bmesh.to_mesh(active_mesh)
        my_bmesh.free()


class ThermalErosionOperator(bpy.types.Operator):
    bl_label = "Thermally Erode Object"
    bl_idname = "object.thermal_erosion_operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        self.wiggle_object(context)
        return {'FINISHED'}

    def wiggle_object(self, context):

        active_obj = context.active_object
        active_mesh = active_obj.data
        my_bmesh = bmesh.new()
        my_bmesh.from_mesh(active_mesh)

        # Erosion
        erosion.basic_thermal_erosion(my_bmesh)

        my_bmesh.to_mesh(active_mesh)
        my_bmesh.free()


class MyPluginPanel(bpy.types.Panel):
    bl_label = "My Plugin"
    bl_idname = "OBJECT_PT_my_plugin"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "My Plugin"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Create new terrain")

        row = layout.row()
        row.operator("object.create_terrain_operator")

        row = layout.row()
        row.label(text="Displacement")

        obj = context.active_object
        if obj is None:
            return

        obj_properties = obj.my_obj_props

        row = layout.row()
        row.prop(obj_properties, "displacement")

        layout.separator()

        row = layout.row()
        row.operator("object.update_terrain_operator")

        row = layout.row()
        row.operator("object.animate_object_operator")

        row = layout.row()
        row.operator("object.wiggle_object_operator")

        row = layout.row()
        row.operator("object.thermal_erosion_operator")


class MyObjectPropertiesGroup(bpy.types.PropertyGroup):
    displacement: FloatProperty(name="Displacement", default=1, min=0.1, max=10, description="A description of displacement property")
    old_displacement: FloatProperty(name="Old Displacement", default=1, min=0.1, max=10, description="A description of old displacement property")
