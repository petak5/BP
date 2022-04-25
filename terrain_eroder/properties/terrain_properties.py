"""
Note: some property name and desciption texts were sourced from Bleder's documentation: https://docs.blender.org/api/current/mathutils.noise.html
"""

import bpy
from bpy.props import (
    IntProperty,
    FloatProperty,
    BoolProperty,
    EnumProperty
)


class TerrainProperties(bpy.types.PropertyGroup):
    __random_method_items = [
        ("CELL", "Cell", "Cell Method"),
        ("FRACTAL", "Fractal", "Fractal Method"),
        ("HETERO_TERRAIN", "Hetero Terrain", "Hetero Terrain Method"),
        ("HYBRID_MULTI_FRACTAL", "Hybrid Multifractal", "Hybrid Multifractal Method"),
        ("MULTI_FRACTAL", "Multifractal", "Multifractal Method"),
        ("NOISE", "Noise", "Noise Method"),
        ("RIDGED_MULTI_FRACTAL", "Ridged Multifractal", "Ridged Multifractal Method"),
        ("TURBULENCE", "Turbulence", "Turbulence Method"),
        ("VARIABLE_LACUNARITY", "Variable Lacunarity", "Variable Lacunarity Method")
    ]
    random_method: EnumProperty(
        items=__random_method_items,
        name="Method",
        description="Randomness method"
    )
    seed: IntProperty(
        name="Seed",
        default=1,
        min=0,
        description="Seed for the random function (when set at 0, the current time is used as seed)"
    )
    noise_scale: FloatProperty(
        name="Noise Scale",
        default=0.05,
        description="The resolution of the noise"
    )
    # Dimensions
    size_x: IntProperty(
        name="Size X",
        default=100,
        min=2,
        soft_max=1000,
        description="Number of vertices in the X direction"
    )
    size_y: IntProperty(
        name="Size Y",
        default=100,
        min=2,
        soft_max=1000,
        description="Number of vertices in the Y direction"
    )
    # Step size
    step_x: FloatProperty(
        name="Step X",
        default=0.05,
        description="Size of steps on X axis"
    )
    step_y: FloatProperty(
        name="Step Y",
        default=0.05,
        description="Size of steps on Y axis"
    )

    ###################
    # Method Specific #
    ###################
    __noise_basis_items = [
        ("BLENDER", "Blender", "Blender Noise Type"),
        ("PERLIN_ORIGINAL", "Perlin Original", "Perlin Original Noise Type"),
        ("PERLIN_NEW", "Perlin New", "Perlin New Noise Type"),
        ("VORONOI_F1", "Voronoi F1", "Voronoi F1 Noise Type"),
        ("VORONOI_F2", "Voronoi F2", "Voronoi F2 Noise Type"),
        ("VORONOI_F3", "Voronoi F3", "Voronoi F3 Noise Type"),
        ("VORONOI_F4", "Voronoi F4", "Voronoi F4 Noise Type"),
        ("VORONOI_F2F1", "Voronoi F2F1", "Voronoi F2F1 Noise Type"),
        ("VORONOI_CRACKLE", "Voronoi Crackle", "Voronoi Crackle Noise Type"),
        ("CELLNOISE", "Cellnoise", "Cellnoise Noise Type")
    ]
    noise_basis: EnumProperty(
        items=__noise_basis_items,
        name="Noise Basis",
        default=__noise_basis_items[1][0],
        description="Type of noise provided to the randomness method"
    )
    h: FloatProperty(
        name="H",
        default=1,
        description="Fractal dimension of the roughest areas"
    )
    lacunarity: FloatProperty(
        name="Lacunarity",
        default=2,
        description="Gap between frequencies"
    )
    octaves: IntProperty(
        name="Octaves",
        default=8,
        min=1,
        description="Number of frequencies used"
    )
    offset: FloatProperty(
        name="Offset",
        default=0,
        description="Height of the terrain above the 'sea level'"
    )
    gain: FloatProperty(
        name="Gain",
        default=1,
        description="Scale of the values"
    )

    ##############
    # Turbulence #
    ##############
    hard: BoolProperty(
        name="Hard",
        default=True,
        description="Determines whether the turbulencies are hard (sharp edges) or not (smooth edges)"
    )
    amplitude_scale: FloatProperty(
        name="Amplitude Scale",
        default=0.5,
        description="Amplitude scaling factor"
    )
    frequency_scale: FloatProperty(
        name="Frequency Scale",
        default=2,
        description="Frequency scaling factor"
    )

    #######################
    # Variable Lacunarity #
    #######################
    distortion: FloatProperty(
        name="Distortion",
        default=1,
        description="The ammount of distortion"
    )
    noise_type_1: EnumProperty(
        items=__noise_basis_items,
        name="Noise Type 1",
        default=__noise_basis_items[1][0],
        description="Type of 1st noise provided to the randomness method"
    )
    noise_type_2: EnumProperty(
        items=__noise_basis_items,
        name="Noise Type 2",
        default=__noise_basis_items[1][0],
        description="Type of 2nd noise provided to the randomness method"
    )
