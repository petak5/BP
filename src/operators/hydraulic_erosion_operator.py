import bpy
import bmesh
from ..erosions.hydraulic_erosion import hydraulic_erosion


class HydraulicErosionOperator(bpy.types.Operator):
    bl_label = "Hydraulic Erosion"
    bl_idname = "object.hydraulic_erosion_operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        self.erode(context)
        return {'FINISHED'}

    def erode(self, context):

        active_obj = context.active_object
        active_mesh = active_obj.data
        my_bmesh = bmesh.new()
        my_bmesh.from_mesh(active_mesh)

        # Erosion
        hydraulic_erosion(my_bmesh)

        my_bmesh.to_mesh(active_mesh)
        my_bmesh.free()
