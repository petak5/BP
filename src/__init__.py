# bl_info has to be defined here, otherwise the plugin won't show in settings
bl_info = {
    "name": "Eroder",
    "author": "Peter Urgos",
    "version": (0, 0, 1),
    "blender": (2, 93, 0),
    "location": "View3D > Sidebar > Example Tab",
    "description": "Add-on for terrain erosion",
    "category": "3D View"
}


from multiprocessing import current_process
if current_process().name != "MainProcess":
    from .erosions.thermal_erosion_method import do_stuff, calculate_erosion
else:
    print("Executing...")
    import bpy
    from bpy.props import PointerProperty

    from .panels.my_plugin_panel import classes
    from .properties.erosion_properties import ErosionProperties


    def register():
        for cls in classes:
            bpy.utils.register_class(cls)
        bpy.types.Scene.erosion_properties = PointerProperty(type=ErosionProperties, name="Erosion Properties", description="Properties of erosion")


    def unregister():
        for cls in reversed(classes):
            bpy.utils.unregister_class(cls)


    if __name__ == "__main__":
        register()
