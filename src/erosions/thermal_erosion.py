import bpy
import bmesh
import numpy as np
from math import sqrt
from datetime import datetime
import time
import concurrent.futures
from multiprocessing import Pool, cpu_count

from .tools import edge_get_neighbour_vertex, bmesh_to_mesh, mesh_to_bmesh
from .thermal_erosion_method import calculate_erosion
from ..model.types import Mesh, INDEX_ID, INDEX_X, INDEX_Y, INDEX_Z, ErosionStatus


class ThermalErosionSettings:
    iterations: int
    max_slope: float
    erosion_strength: float


# `ctrl+a -> scale` to apply scale transformation before calling this function
def thermal_erosion(context: bpy.types.Context, settings: ThermalErosionSettings, erosion_status: ErosionStatus):
    obj: bpy.types.Object = context.active_object

    active_mesh = obj.data
    my_bmesh = bmesh.new()
    my_bmesh.from_mesh(active_mesh)
    my_bmesh.verts.ensure_lookup_table()

    # mesh = bmesh_to_mesh(my_bmesh)

    # Call func
    # _thermal_erosion(mesh, settings)
    thermal_erosion_old(my_bmesh, settings, erosion_status)

    # """test"""
    # start = time.perf_counter()
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     for i in range(1, 11):
    #         results = [executor.submit(do_stuff) for _ in range(8)]

    #         for f in concurrent.futures.as_completed(results):
    #             print(f.result())

    #         properties.progress = i * 10
    #         print(f"Done {i} of 10")

    #     print("All done")

    # # p1 = multiprocessing.Process(target=do_stuff)
    # # p1.start()
    # # p1.join()

    # finish = time.perf_counter()
    # print(f"Finished in '{round(finish - start, 2)}' second(s)")
    # """end test"""

    # TODO: I uncommented this to use the old method
    # mesh_to_bmesh(mesh, my_bmesh)

    my_bmesh.to_mesh(active_mesh)
    my_bmesh.free()

    context.area.tag_redraw()
    erosion_status.is_running = False


def _thermal_erosion(mesh: Mesh, settings: ThermalErosionSettings):
    start_time = datetime.now()

    """ Debug """
    if True:
        temp_sum = np.sum(mesh.vertices["z"])
        print(f"Before = {temp_sum}")
    """ Debug end """

    # Grid size
    # N = 50
    # Talus threshold
    # T = 4/N
    # T = 0.3
    # C = 0.001
    T = settings.max_slope / 100
    C = settings.erosion_strength

    iterations = settings.iterations

    try:
        workers = cpu_count()
    except NotImplementedError:
        workers = 1

    # with Pool(processes=workers) as pool:
    #     for iter in range(iterations):
    #         deltas = np.zeros(len(mesh.vertices), dtype=float)

    #         results = [pool.apply(calculate_erosion, [vert, [mesh.vertices[id_neigh] for id_neigh in vert.neighbours], T, C]) for vert in mesh.vertices.values()]

    #         for result in results:
    #             # Apply changes to deltas
    #             for key, value in result.items():
    #                 deltas[key] += value

    #         # Apply deltas to mesh
    #         for i in range(len(deltas)):
    #             # print(deltas)
    #             mesh.vertices[key].z += deltas[i]

    #         print(f"Done {iter} of {iterations}")

    #     print("All done")

    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        count = mesh.vertices.size
        bounds = []
        for i in range(1, workers):
            bounds.append(int(count/workers * i))
        bounds.append(count)
        # print(f"{count} x {workers} -- {bounds}")

        for iter in range(iterations):
            deltas = np.zeros(shape=mesh.vertices.shape, dtype=float)


            # results: list[concurrent.futures.Future] = []
            # b_old = 0
            # for b in bounds:
            #     results.append(executor.submit(calculate_erosion, mesh.vertices[b_old:b], T, C))
            #     b_old = b

            # results = [executor.submit(calculate_erosion, vert, T, C) for vert in mesh.vertices]
            # results = [ executor.submit(calculate_erosion, mesh.vertices[ : mesh.vertices.size//4], T, C),
            #             executor.submit(calculate_erosion, mesh.vertices[mesh.vertices.size//4 : mesh.vertices.size//2], T, C),
            #             executor.submit(calculate_erosion, mesh.vertices[mesh.vertices.size//2 : mesh.vertices.size//4 * 3], T, C),
            #             executor.submit(calculate_erosion, mesh.vertices[mesh.vertices.size//4 * 3:], T, C)]

            results = [executor.submit(calculate_erosion, mesh, T, C)]

            for f in concurrent.futures.as_completed(results):
                result_deltas = f.result()

                # Apply changes to deltas
                for i in range(result_deltas.size):
                    deltas[i] += result_deltas[i]

            # Apply deltas to mesh
            # TODO: convert this to single expression
            # TODO: `mesh.vertices["z"] += deltas`
            for i in range(deltas.size):
                # print(deltas)
                mesh.vertices[i][INDEX_Z] += deltas[i]

            print(f"Done {iter} of {iterations}")

        print("All done")

    """ Debug """
    if True:
        temp_sum = np.sum(mesh.vertices["z"])
        print(f"After = {temp_sum}")
    """ Debug end """

    print(datetime.now() - start_time)


def thermal_erosion_old(mesh: bmesh.types.BMesh, settings: ThermalErosionSettings, erosion_status: ErosionStatus):
    """ Debug """
    if True:
        temp_sum = 0
        for i in range(len(mesh.verts)):
            temp_sum += mesh.verts[i].co.z
        print(f"Before = {temp_sum}")
    """ Debug end """

    # Grid size
    # N = 50
    # Talus threshold
    # T = 4/N
    # T = 0.3
    # C = 0.001
    T = settings.max_slope / 100
    C = settings.erosion_strength

    iterations = settings.iterations

    for iter in range(iterations):

        delta = np.zeros(len(mesh.verts), dtype=float)

        for i in range(len(mesh.verts)):
            v = mesh.verts[i]

            d_total = 0
            d_max = 0
            angle_max = 0

            for j in range(len(v.link_edges)):
                v_neigh = edge_get_neighbour_vertex(v, j)

                # height delta
                d = v.co.z - v_neigh.co.z
                xy_distance = sqrt(pow(v.co.x - v_neigh.co.x, 2) + pow(v.co.y - v_neigh.co.y, 2))
                angle = d / xy_distance

                if angle > T:
                    d_total += d

                    if angle > angle_max:
                        angle_max = angle
                    if d > d_max:
                        d_max = d

            for j in range(len(v.link_edges)):
                v_neigh = edge_get_neighbour_vertex(v, j)

                # height delta
                d = v.co.z - v_neigh.co.z
                xy_distance = sqrt(pow(v.co.x - v_neigh.co.x, 2) + pow(v.co.y - v_neigh.co.y, 2))
                angle = d / xy_distance

                if angle > T:
                    # move_by = C * (d_max - T) * (d / d_total)
                    move_by = angle * C * (d / d_total)

                    delta[v_neigh.index] += move_by
                    delta[v.index] -= move_by

        for i in range(len(mesh.verts)):
            v = mesh.verts[i]

            v.co.z += delta[i]

        erosion_status.progress = round(100 * iter / iterations)
        if erosion_status.stop_requested:
            return

    """ Debug """
    if True:
        temp_sum = 0
        for i in range(len(mesh.verts)):
            temp_sum += mesh.verts[i].co.z
        print(f"After = {temp_sum}")
    """ Debug end """

    erosion_status.is_running = False
