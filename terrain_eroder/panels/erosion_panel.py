import bpy

from terrain_eroder.properties.erosion_properties import ErosionProperties


class ErosionPanel(bpy.types.Panel):
    bl_label = "Terrain Erosion"
    bl_idname = "OBJECT_PT_terrain_erosion"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"
    bl_category = "Eroder"

    def draw(self, context: bpy.types.Context):
        layout = self.layout

        view_layer = bpy.context.view_layer
        # Check active object and its type (must be MESH)
        if len(view_layer.objects.selected) <= 0 or view_layer.objects.active is None or view_layer.objects.active.type != "MESH":
            row = layout.row()
            row.label(text="Select a mesh object for erosion", icon="INFO")
            return

        obj = view_layer.objects.active
        properties: ErosionProperties = context.scene.erosion_properties

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

            # row = layout.row()
            # row.prop(properties, "hypb_erosion_strength")

            row = layout.row()
            row.prop(properties, "use_vertex_groups")
            if properties.use_vertex_groups:
                layout.template_list("UI_UL_list", "my_custom_id", obj, "vertex_groups", obj.vertex_groups, "active_index")

            method_operator_name = "object.erosion_operator"

        layout.separator()

        if properties.is_running:
            row = layout.row()
            row.prop(properties, "progress", slider=True)

            row = layout.row()
            row.label(text="Erosion in progress", icon="SORTTIME")

            row = layout.row()
            row.label(text="To abort press ESC or RIGHTMOUSE")

            row = layout.row()
            row.label(text=f"Time elapsed: {properties.elapsed_time}", icon="TIME")
        else:
            row = layout.row()
            row.operator(method_operator_name, icon="PLAY")

            if properties.last_time != "":
                row = layout.row()
                row.label(text=f"Last time: {properties.last_time}", icon="TIME")
