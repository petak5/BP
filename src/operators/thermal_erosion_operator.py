import bpy
import bmesh
from ..erosions.thermal_erosion import thermal_erosion


class ThermalErosionOperator(bpy.types.Operator):
    bl_label = "Thermall Erosion"
    bl_idname = "object.thermal_erosion_operator"

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
        thermal_erosion(my_bmesh)

        my_bmesh.to_mesh(active_mesh)
        my_bmesh.free()
