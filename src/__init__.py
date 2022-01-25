import bpy
from bpy.props import PointerProperty

from .panels.my_plugin_panel import classes
from .panels.my_plugin_panel import MyObjectPropertiesGroup


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


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
