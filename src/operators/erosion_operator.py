import bpy
import bmesh
from ..erosions.thermal_erosion import thermal_erosion, ThermalErosionSettings
from ..erosions.hydraulic_erosion import hydraulic_erosion, HydraulicErosionSettings
from ..properties.erosion_properties import ErosionProperties


class ErosionOperator(bpy.types.Operator):
    bl_label = "Erode"
    bl_idname = "object.erosion_operator"
    bl_description = "Erode using selected method"

    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.edit_object is None

    def execute(self, context):
        self.main(context)
        return {'FINISHED'}

    def main(self, context: bpy.types.Context):
        obj: bpy.types.Object = context.active_object
        scene = context.scene

        active_mesh = obj.data
        my_bmesh = bmesh.new()
        my_bmesh.from_mesh(active_mesh)

        properties: ErosionProperties = scene.erosion_properties

        # Thermal erosion
        if properties.erosion_method == "THERMAL":
            settings = ThermalErosionSettings()
            settings.iterations = properties.th_iterations
            settings.max_slope = properties.th_max_slope
            settings.erosion_strength = properties.th_erosion_strength

            thermal_erosion(my_bmesh, settings)
        # Hydraulic erosion
        else:
            settings = HydraulicErosionSettings()
            settings.iterations = properties.hy_iterations
            settings.rain_intensity = properties.hy_rain_intensity
            settings.soil_solubility = properties.hy_soil_solubility
            settings.evaporation_intensity = properties.hy_evaporation_intensity
            settings.sediment_capacity = properties.hy_sediment_capacity
            if properties.use_vertex_groups:
                # Source: https://blender.stackexchange.com/a/75240 (https://blender.stackexchange.com/questions/75223/finding-vertices-in-a-vertex-group-using-blenders-python-api)
                # vg_idx = obj.vertex_groups.active_index
                # indices: list[int] = [ v.index for v in obj.data.vertices if vg_idx in [ vg.group for vg in v.groups ] ]
                indices: list[int] = []
                for v in obj.data.vertices:
                    if len(v.groups) > 0:
                        indices.append(v.index)
                settings.selected_vertex_indices = indices

            hydraulic_erosion(my_bmesh, settings)

        my_bmesh.to_mesh(active_mesh)
        my_bmesh.free()
