import bpy


class ErosionPanel(bpy.types.Panel):
    bl_label = "Terrain Erosion"
    bl_idname = "OBJECT_PT_tarrain_erosion"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Erosion"

    def draw(self, context):
        layout = self.layout

        if len(context.selected_objects) <= 0:
            return
        obj = context.selected_objects[0]
        properties = obj.erosion_properties

        # row = layout.row()
        # row.label(text="Erode terrain")

        row = layout.row()
        row.prop(properties, "erosion_method")

        layout.separator()

        # Thermal erosion
        if properties.erosion_method == "THERMAL":
            row = layout.row()
            row.prop(properties, "th_iterations")

            row = layout.row()
            row.prop(properties, "th_max_slope")

            row = layout.row()
            row.prop(properties, "th_erosion_strength")

            layout.separator()

            row = layout.row()
            row.operator("object.erosion_operator")
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

            layout.separator()

            row = layout.row()
            row.operator("object.erosion_operator")
