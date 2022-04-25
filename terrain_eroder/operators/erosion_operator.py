import bpy
import bmesh
from datetime import datetime
from threading import Thread

from ..erosions.thermal_erosion import thermal_erosion_old, ThermalErosionSettings
from ..erosions.hydraulic_erosion import hydraulic_erosion, HydraulicErosionSettings
from ..erosions.hydraulic_erosion_pb import hydraulic_erosion_pb, HydraulicErosionPBSettings
from ..properties.erosion_properties import ErosionProperties
from ..erosions.tools import bmesh_to_mesh, mesh_to_bmesh
from ..model.types import Mesh, ErosionStatus


class ErosionOperator(bpy.types.Operator):
    bl_label = "Erode"
    bl_idname = "object.erosion_operator"
    bl_description = "Erode using selected method"

    erosion_status: ErosionStatus = ErosionStatus()
    thread: Thread = None
    mesh: Mesh = None
    my_bmesh: bmesh.types.BMesh = None
    use_custom_mesh_object = False

    __start_time: datetime = None

    __timer: bpy.types.Timer = None


    @classmethod
    def poll(self, context: bpy.types.Context):
        return context.selected_objects and context.edit_object is None and not self.erosion_status.is_running


    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        wm = context.window_manager
        self.__timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)

        self.__start_time = datetime.now()

        self.start_erosion(context)

        return {"RUNNING_MODAL"}


    def modal(self, context: bpy.types.Context, event: bpy.types.Event):
        if event.type in ["RIGHTMOUSE", "ESC"]:
            self.stop_erosion(context, abort=True)
            return {'CANCELLED'}
        elif event.type in ['TIMER']:
            self.update_progress(context)

            if not self.erosion_status.is_running:
                self.stop_erosion(context)
                return {"FINISHED"}

        return {"PASS_THROUGH"}


    def update_progress(self, context: bpy.types.Context):
        properties: ErosionProperties = context.scene.erosion_properties
        properties.progress = self.erosion_status.progress

        time_total = datetime.now() - self.__start_time
        minutes, seconds = divmod(time_total.seconds, 60)
        miliseconds, _ = divmod(time_total.microseconds, 1000)
        properties.elapsed_time = "{:02d}:{:02d}.{:03d}".format(minutes, seconds, miliseconds)


    def stop_erosion(self, context: bpy.types.Context, abort=False):
        if abort:
            self.erosion_status.stop_requested = True

        self.thread.join()
        self.thread = None

        if not abort:
            self.finish_erosion(context)

        properties: ErosionProperties = context.scene.erosion_properties
        properties.is_running = False
        properties.progress = 0

        self.erosion_status.is_running = False
        self.erosion_status.progress = 0
        self.erosion_status.stop_requested = False

        time_total = datetime.now() - self.__start_time
        minutes, seconds = divmod(time_total.seconds, 60)
        miliseconds, _ = divmod(time_total.microseconds, 1000)
        properties.last_time = "{:02d}:{:02d}.{:03d}".format(minutes, seconds, miliseconds)
        print(time_total)

        wm = context.window_manager
        wm.event_timer_remove(self.__timer)


    def start_erosion(self, context: bpy.types.Context):
        obj: bpy.types.Object = context.active_object
        active_mesh = obj.data
        self.my_bmesh = bmesh.new()
        self.my_bmesh.from_mesh(active_mesh)
        self.my_bmesh.verts.ensure_lookup_table()

        self.mesh = bmesh_to_mesh(self.my_bmesh)

        settings = None
        target = None
        args = None
        properties: ErosionProperties = context.scene.erosion_properties

        # Thermal erosion
        if properties.erosion_method == "THERMAL":
            settings                  = ThermalErosionSettings()
            settings.iterations       = properties.th_iterations
            settings.max_slope        = properties.th_max_slope
            settings.erosion_strength = properties.th_erosion_strength

            target = thermal_erosion_old
            args = [self.my_bmesh, settings]
        # Hydraulic erosion - grid based
        elif properties.erosion_method == "HYDRAULIC":
            settings = HydraulicErosionSettings()
            settings.iterations            = properties.hy_iterations
            settings.rain_intensity        = properties.hy_rain_intensity
            settings.soil_solubility       = properties.hy_soil_solubility
            settings.evaporation_intensity = properties.hy_evaporation_intensity
            settings.sediment_capacity     = properties.hy_sediment_capacity
            if properties.use_vertex_groups:
                # Source: https://blender.stackexchange.com/a/75240 (https://blender.stackexchange.com/questions/75223/finding-vertices-in-a-vertex-group-using-blenders-python-api)
                # vg_idx = obj.vertex_groups.active_index
                # indices: list[int] = [ v.index for v in obj.data.vertices if vg_idx in [ vg.group for vg in v.groups ] ]
                indices: list[int] = []
                for v in obj.data.vertices:
                    if len(v.groups) > 0:
                        indices.append(v.index)
                settings.selected_vertex_indices = indices

            target = hydraulic_erosion
            args = [self.my_bmesh, settings]
        # Hydraulic erosion - particle based
        else:
            settings = HydraulicErosionPBSettings()
            settings.rain_intensity             = properties.hypb_rain_intensity
            settings.drop_size                  = properties.hypb_drop_size
            settings.drop_max_steps             = properties.hypb_drop_max_steps
            settings.drop_evaporation_intensity = properties.hypb_drop_evaporation_intensity
            settings.erosion_strength           = properties.hypb_erosion_strength

            target = hydraulic_erosion_pb
            args = [self.mesh, settings]
            self.use_custom_mesh_object = True

        properties.progress = 0
        properties.is_running = True

        self.erosion_status.is_running = True
        args.append(self.erosion_status)
        self.thread = Thread(target=target, args=args)
        self.thread.start()


    # Convert Mesh back to Object
    def finish_erosion(self, context: bpy.types.Context):
        obj: bpy.types.Object = context.active_object

        active_mesh = obj.data
        if self.use_custom_mesh_object:
            mesh_to_bmesh(self.mesh, self.my_bmesh)

        self.my_bmesh.to_mesh(active_mesh)
        self.my_bmesh.free()

        context.area.tag_redraw()
