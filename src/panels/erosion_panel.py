import bpy


class ErosionPanel(bpy.types.Panel):
    bl_label = "Terrain Erosion"
    bl_idname = "OBJECT_PT_tarrain_erosion"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Erosion"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Erode terrain")

        row = layout.row()
        row.operator("object.thermal_erosion_operator")

        row = layout.row()
        row.operator("object.hydraulic_erosion_operator")
