print("Executing __init__.py...")

import bpy
from bpy.props import PointerProperty

from .panels.my_plugin_panel import CreatorPanel, AnimateObjectOperator
from .panels.erosion_panel import ErosionPanel
from .operators.create_terrain_operator import CreateTerrainOperator
from .operators.erosion_operator import ErosionOperator
from .properties.terrain_properties import TerrainProperties
from .properties.erosion_properties import ErosionProperties


bl_info = {
    "name": "Terrain Eroder",
    "author": "Peter Urgos",
    "version": (0, 1, 0),
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
