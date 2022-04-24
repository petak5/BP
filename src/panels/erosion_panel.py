import bpy

from ..properties.erosion_properties import ErosionProperties


class ErosionPanel(bpy.types.Panel):
    bl_label = "Terrain Erosion"
    bl_idname = "OBJECT_PT_terrain_erosion"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Erosion"

    def draw(self, context: bpy.types.Context):
        layout = self.layout

        if len(context.selected_objects) <= 0:
            row = layout.row()
            row.label(text="Select an object for erosion")
            return
        obj = context.selected_objects[0]
        scene = context.scene
        properties: ErosionProperties = scene.erosion_properties

        row = layout.row()
        row.prop(properties, "erosion_method")

        layout.separator()

        # Name of the operator for selected erosion method
        method_operator_name = ""

        # Thermal erosion
        if properties.erosion_method == "THERMAL":
            row = layout.row()
            row.prop(properties, "th_iterations")

            row = layout.row()
            row.prop(properties, "th_max_slope")

            row = layout.row()
            row.prop(properties, "th_erosion_strength")

            method_operator_name = "object.erosion_operator"
        # Hydraulic erosion - grid based
        elif properties.erosion_method == "HYDRAULIC":
            layout.separator()

            row = layout.row()
            row.prop(properties, "hy_iterations")

            row = layout.row()
            row.prop(properties, "hy_rain_intensity")

            row = layout.row()
            row.prop(properties, "hy_soil_solubility")

            row = layout.row()
            row.prop(properties, "hy_evaporation_intensity")

            row = layout.row()
            row.prop(properties, "hy_sediment_capacity")

            row = layout.row()
            row.prop(properties, "use_vertex_groups")
            if properties.use_vertex_groups:
                layout.template_list("UI_UL_list", "my_custom_id", obj, "vertex_groups", obj.vertex_groups, "active_index")

            method_operator_name = "object.erosion_operator"
        # Hydraulic erosion - particle based
        else:
            layout.separator()

            row = layout.row()
            row.prop(properties, "hypb_rain_intensity")

            row = layout.row()
            row.prop(properties, "hypb_drop_size")

            row = layout.row()
            row.prop(properties, "hypb_drop_max_steps")

            row = layout.row()
            row.prop(properties, "hypb_drop_evaporation_intensity")

            row = layout.row()
            row.prop(properties, "hypb_erosion_strength")

            method_operator_name = "object.erosion_operator"

        layout.separator()

        row = layout.row()
        row.operator(method_operator_name, icon="PLAY")

        if properties.is_running:
            row = layout.row()
            row.label(text="Erosion in progress", icon="SORTTIME")

            row = layout.row()
            row.prop(properties, "progress")

            row = layout.row()
            row.label(text=f"Time elapsed: {properties.elapsed_time}", icon="TIME")
        elif properties.last_time != "":
            row = layout.row()
            row.label(text=f"Last time: {properties.last_time}", icon="TIME")
