import bpy
from bpy.props import (
    BoolProperty,
    IntProperty,
    FloatProperty,
    EnumProperty
)


class ErosionProperties(bpy.types.PropertyGroup):
    #####################
    # Common properties #
    #####################
    _erosion_method_items = [
        ("THERMAL", "Thermal", "Thermal erosion"),
        ("HYDRAULIC", "Hydraulic", "Hydraulic Erosion")
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

    #####################
    # Hydraulic erosion #
    #####################
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
