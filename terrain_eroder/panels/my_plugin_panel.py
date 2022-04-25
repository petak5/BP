import bpy
import bmesh
import random


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
    bl_label = "Terrain Creator"
    bl_idname = "OBJECT_PT_terrain_creator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Eroder"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Create new terrain")

        row = layout.row()
        row.operator("object.create_terrain_operator")

        if len(context.selected_objects) <= 0:
            return

        row = layout.row()
        row.operator("object.wiggle_object_operator")
