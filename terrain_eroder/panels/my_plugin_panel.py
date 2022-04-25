import bpy

from ..properties.terrain_properties import TerrainProperties


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


class CreatorPanel(bpy.types.Panel):
    bl_label = "Terrain Creator"
    bl_idname = "OBJECT_PT_terrain_creator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Eroder"

    def draw(self, context):
        properties: TerrainProperties = context.scene.terrain_properties
        layout = self.layout

        row = layout.row()
        row.label(text="Noise settings")

        row = layout.row()
        row.prop(properties, "random_method")

        if properties.random_method in ["FRACTAL", "HETERO_TERRAIN", "HYBRID_MULTI_FRACTAL", "MULTI_FRACTAL", "NOISE", "RIDGED_MULTI_FRACTAL", "TURBULENCE"]:
            row = layout.row()
            row.prop(properties, "noise_basis")

        if properties.random_method in ["FRACTAL", "HETERO_TERRAIN", "HYBRID_MULTI_FRACTAL", "MULTI_FRACTAL", "RIDGED_MULTI_FRACTAL"]:
            row = layout.row()
            row.prop(properties, "h")
            row = layout.row()
            row.prop(properties, "lacunarity")

        if properties.random_method in ["FRACTAL", "HETERO_TERRAIN", "HYBRID_MULTI_FRACTAL", "MULTI_FRACTAL", "RIDGED_MULTI_FRACTAL", "TURBULENCE"]:
            row = layout.row()
            row.prop(properties, "octaves")

        if properties.random_method in ["HETERO_TERRAIN", "HYBRID_MULTI_FRACTAL", "RIDGED_MULTI_FRACTAL"]:
            row = layout.row()
            row.prop(properties, "offset")

        if properties.random_method in ["HYBRID_MULTI_FRACTAL", "RIDGED_MULTI_FRACTAL"]:
            row = layout.row()
            row.prop(properties, "gain")

        if properties.random_method in ["TURBULENCE"]:
            row = layout.row()
            row.prop(properties, "hard")
            row = layout.row()
            row.prop(properties, "amplitude_scale")
            row = layout.row()
            row.prop(properties, "frequency_scale")

        if properties.random_method in ["VARIABLE_LACUNARITY"]:
            row = layout.row()
            row.prop(properties, "distortion")
            row = layout.row()
            row.prop(properties, "noise_type_1")
            row = layout.row()
            row.prop(properties, "noise_type_2")

        layout.separator()

        row = layout.row()
        row.label(text="General noise settings")

        row = layout.row()
        row.prop(properties, "seed")
        row = layout.row()
        row.prop(properties, "noise_scale")

        layout.separator()

        row = layout.row()
        row.label(text="Mesh settings")

        row = layout.row()
        row.prop(properties, "size_x")
        row.prop(properties, "size_y")

        row = layout.row()
        row.prop(properties, "step_x")
        row.prop(properties, "step_y")

        layout.separator()

        row = layout.row()
        row.operator("object.create_terrain_operator", icon="SCENE_DATA")
