import bpy


class ErosionPanel(bpy.types.Panel):
    bl_label = "Terrain Erosion"
    bl_idname = "OBJECT_PT_tarrain_erosion"
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
        properties = scene.erosion_properties

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
        # Hydraulic erosion
        else:
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

        layout.separator()

        row = layout.row()
        row.operator(method_operator_name)