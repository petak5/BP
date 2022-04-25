print("Executing __init__.py...")

import bpy
from bpy.props import PointerProperty

from terrain_eroder.panels.creator_panel import CreatorPanel, AnimateObjectOperator
from terrain_eroder.panels.erosion_panel import ErosionPanel
from terrain_eroder.operators.create_terrain_operator import CreateTerrainOperator
from terrain_eroder.operators.erosion_operator import ErosionOperator
from terrain_eroder.properties.terrain_properties import TerrainProperties
from terrain_eroder.properties.erosion_properties import ErosionProperties


bl_info = {
    "name": "Terrain Eroder",
    "author": "Peter Urgos",
    "version": (0, 2, 0),
    "blender": (2, 93, 0),
    "location": "View3D > Sidebar > Eroder",
    "description": "Add-on for terrain erosion",
    "category": "3D View"
}


# Classes inheriting from Blender that need to be (de-)activated
classes = (
    TerrainProperties,
    ErosionProperties,
    CreateTerrainOperator,
    AnimateObjectOperator,
    ErosionOperator,
    CreatorPanel,
    ErosionPanel
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.erosion_properties = PointerProperty(type=ErosionProperties, name="Erosion Properties", description="Properties of erosion")
    bpy.types.Scene.terrain_properties = PointerProperty(type=TerrainProperties, name="Terrain Properties", description="Properties for terrain creation")


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
