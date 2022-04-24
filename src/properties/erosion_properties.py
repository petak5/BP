import bpy
from bpy.props import (
    BoolProperty,
    IntProperty,
    FloatProperty,
    EnumProperty,
    StringProperty
)


def update_ui(self, context: bpy.types.Context):
    region: bpy.types.Region
    for region in context.area.regions:
        if region.type == "UI":
            region.tag_redraw()
    return None


class ErosionProperties(bpy.types.PropertyGroup):
    #####################
    # Common properties #
    #####################
    _erosion_method_items = [
        ("THERMAL", "Thermal", "Thermal Erosion"),
        ("HYDRAULIC", "Hydraulic", "Hydraulic Erosion"),
        ("HYDRAULIC-PB", "Hydraulic Particle Based", "Hydraulic Erosion - Particle Based")

    ]
    erosion_method: EnumProperty(
        items=_erosion_method_items,
        name="Method",
        # default=_erosion_method_items[1][0],
        description="The method of erosion simultaion"
    )
    use_vertex_groups: BoolProperty(
        name="Use Vertex Group(s)",
        default=False,
        description="Define area of effect using vertex group(s)"
    )
    is_running: BoolProperty(
        name="Running",
        default=False,
        description="Is erosion running"
    )
    progress: IntProperty(
        name="Progress",
        default=0,
        min=0,
        max=100,
        description="Progress of the running erosion",
        update=update_ui
    )
    elapsed_time: StringProperty(
        name="Elapsed Time",
        default="",
        description="Elapsed time of the running erosion"
    )
    last_time: StringProperty(
        name="Last Time",
        default="",
        description="Duration of the last ran erosion"
    )

    ###################
    # Thermal erosion #
    ###################
    th_iterations: IntProperty(
        name="Iterations",
        default=100,
        min=1,
        description="Number of erosion iterations"
    )
    th_max_slope: FloatProperty(
        name="Max Slope",
        default=30,
        min=0,
        max=100,
        description="Maximum Slope Angle after which soil starts to slide down"
    )
    th_erosion_strength: FloatProperty(
        name="Erosion Strength",
        default=0.001,
        min=0.000001,
        max=1,
        description="Affects how much soil is moved"
    )

    ##################################
    # Hydraulic erosion - grid based #
    ##################################
    hy_iterations: IntProperty(
        name="Iterations",
        default=200,
        min=1,
        description="Number of erosion iterations"
    )
    hy_rain_intensity: FloatProperty(
        name="Rain Intensity",
        default=0.01,
        min=0.000001,
        soft_max=1,
        description="Determines how much water falls on vertices each iteration"
    )
    hy_soil_solubility: FloatProperty(
        name="Soil Solubility",
        default=0.01,
        min=0.000001,
        soft_max=1,
        description="TODO TODO TODO"
    )
    # TODO: min could be 0?
    hy_evaporation_intensity: FloatProperty(
        name="Evaporation Intensity",
        default=30,
        min=0.000001,
        max=100,
        description="Percentage of how much water evaporates each iteration"
    )
    hy_sediment_capacity: FloatProperty(
        name="Sediment Capacity",
        default=1,
        min=0.000001,
        max=100,
        description="Percentage of how much sediment can water contain"
    )

    ######################################
    # Hydraulic erosion - particle based #
    ######################################
    hypb_rain_intensity: FloatProperty(
        name="Rain Intensity",
        default=1,
        min=0.000001,
        soft_max=10,
        description="Determines how many drops fall on vertices"
    )
    hypb_drop_size: FloatProperty(
        name="Drop Size",
        default=1,
        min=0.000001,
        soft_max=10,
        description="Drop size determines its starting volume and thus how much sediment it can carry"
    )
    hypb_drop_max_steps: IntProperty(
        name="Drop Max Steps",
        default=20,
        min=1,
        soft_max=100,
        description="Count of how many vertices a drop can travel through in its lifetime"
    )
    hypb_drop_evaporation_intensity: FloatProperty(
        name="Drop Evaporation Intensity",
        default=0.1,
        min=0.000001,
        soft_max=1,
        description="Ratio of how much drop's total volume is evaporated each step"
    )
    hypb_erosion_strength: FloatProperty(
        name="Erosion Strength",
        default=0.1,
        min=0.000001,
        soft_max=1,
        description="Strenght of the erosion"
    )
