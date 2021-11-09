import bpy
from bpy.props import PointerProperty

from . import my_plugin_panel

bl_info = {
    "name": "My Test Addon",
    "author": "Peter Urgos",
    "version": (0, 0, 1),
    "blender": (2, 93, 0),
    "location": "View3D > Sidebar > Example Tab",
    "description": "Example add-on that installs a Python package",
    "category": "3D View"
}

classes = (
    my_plugin_panel.MyObjectPropertiesGroup,
    my_plugin_panel.CreateTerrainOperator,
    my_plugin_panel.UpdateTerrainOperator,
    my_plugin_panel.AnimateObjectOperator,
    my_plugin_panel.WiggleObjectOperator,
    my_plugin_panel.ThermalErosionOperator,
    my_plugin_panel.MyPluginPanel
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Object.my_obj_props = PointerProperty(type=my_plugin_panel.MyObjectPropertiesGroup, name="My Object Properties Group", description="A description of my object properties group")


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()