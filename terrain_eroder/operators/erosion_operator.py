import bpy
import bmesh
from datetime import datetime
from threading import Thread

from terrain_eroder.erosions.thermal_erosion import thermal_erosion, ThermalErosionSettings
from terrain_eroder.erosions.hydraulic_erosion import hydraulic_erosion, HydraulicErosionSettings
from terrain_eroder.erosions.hydraulic_erosion_pb import hydraulic_erosion_pb, HydraulicErosionPBSettings
from terrain_eroder.properties.erosion_properties import ErosionProperties
from terrain_eroder.erosions.erosion_status import ErosionStatus


class ErosionOperator(bpy.types.Operator):
    bl_label = "Erode"
    bl_idname = "object.erosion_operator"
    bl_description = "Erode using selected method"

    erosion_status: ErosionStatus = ErosionStatus()
    thread: Thread = None
    my_bmesh: bmesh.types.BMesh = None

    __start_time: datetime = None

    __timer: bpy.types.Timer = None


    @classmethod
    def poll(self, context: bpy.types.Context):
        view_layer = bpy.context.view_layer
        return view_layer.objects.active is not None and view_layer.objects.active.type == "MESH" and not self.erosion_status.is_running


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
            self.check_thread()

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


    # Check if thread is still running, in case an exception occurs
    def check_thread(self):
        if not self.thread.is_alive():
            self.erosion_status.is_running = False


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

        """ Debug """
        temp_sum = 0
        for i in range(len(self.my_bmesh.verts)):
            temp_sum += self.my_bmesh.verts[i].co.z
        print(f"Before = {temp_sum}")
        """ Debug end """

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

            target = thermal_erosion
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
            args = [self.my_bmesh, settings]

        properties.progress = 0
        properties.is_running = True

        self.erosion_status.is_running = True
        args.append(self.erosion_status)
        self.thread = Thread(target=target, args=args)
        self.thread.start()


    # Convert Mesh back to Object
    def finish_erosion(self, context: bpy.types.Context):
        """ Debug """
        temp_sum = 0
        for i in range(len(self.my_bmesh.verts)):
            temp_sum += self.my_bmesh.verts[i].co.z
        print(f"After  = {temp_sum}")
        """ Debug end """

        obj: bpy.types.Object = context.active_object
        active_mesh = obj.data

        self.my_bmesh.to_mesh(active_mesh)
        self.my_bmesh.free()

        context.area.tag_redraw()
