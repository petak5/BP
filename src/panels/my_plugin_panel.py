import bpy
from bpy.props import FloatProperty
import bmesh
import random

from ..operators.create_terrain_operator import CreateTerrainOperator
from ..operators.thermal_erosion_operator import ThermalErosionOperator
from ..operators.hydraulic_erosion_operator import HydraulicErosionOperator

from .erosion_panel import ErosionPanel

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
            delta = random.random() % 0.5
            if random.random() > 0.5:
                delta = -delta
            v.co.z += delta

        my_bmesh.to_mesh(active_mesh)
        my_bmesh.free()


class MyPluginPanel(bpy.types.Panel):
    bl_label = "Erosion Helper"
    bl_idname = "OBJECT_PT_erosion_helper"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Erosion"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Create new terrain")

        row = layout.row()
        row.operator("object.create_terrain_operator")

        # row = layout.row()
        # row.label(text="Displacement")
        #
        # obj = context.active_object
        # if obj is None:
        #     return
        #
        # obj_properties = obj.my_obj_props
        #
        # row = layout.row()
        # row.prop(obj_properties, "displacement")
        #
        # layout.separator()
        #
        # row = layout.row()
        # row.operator("object.update_terrain_operator")
        #
        # row = layout.row()
        # row.operator("object.animate_object_operator")

        row = layout.row()
        row.operator("object.wiggle_object_operator")

        # row = layout.row()
        # row.operator("object.thermal_erosion_operator")
        #
        # row = layout.row()
        # row.operator("object.hydraulic_erosion_operator")


class MyObjectPropertiesGroup(bpy.types.PropertyGroup):
    displacement: FloatProperty(name="Displacement", default=1, min=0.1, max=10, description="A description of displacement property")
    old_displacement: FloatProperty(name="Old Displacement", default=1, min=0.1, max=10, description="A description of old displacement property")


# Classes inheriting from Blender that need to be (de-)activated
classes = (
    MyObjectPropertiesGroup,
    CreateTerrainOperator,
    UpdateTerrainOperator,
    AnimateObjectOperator,
    WiggleObjectOperator,
    ThermalErosionOperator,
    HydraulicErosionOperator,
    MyPluginPanel,
    ErosionPanel
)
