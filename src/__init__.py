import bpy
from bpy.props import PointerProperty

from .panels.my_plugin_panel import classes
from .panels.my_plugin_panel import MyObjectPropertiesGroup
from .properties.erosion_properties import ErosionProperties


bl_info = {
    "name": "Eroder",
    "author": "Peter Urgos",
    "version": (0, 0, 1),
    "blender": (2, 93, 0),
    "location": "View3D > Sidebar > Example Tab",
    "description": "Add-on for terrain erosion",
    "category": "3D View"
}

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Object.my_obj_props = PointerProperty(type=MyObjectPropertiesGroup, name="My Object Properties Group", description="A description of my object properties group")
    bpy.types.Object.erosion_properties = PointerProperty(type=ErosionProperties, name="Erosion Properties", description="Erosion Properties Description")
    # bpy.types.Scene.p = bpy.props.FloatProperty(name="TestProperty", description="My Test Property Description", default=1.0, min=0.0, max=1.0)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
