import bpy
from bmesh.types import BMesh, BMVert, BMEdge
import numpy as np
from math import sqrt

from terrain_eroder.erosions.erosion_status import ErosionStatus


class ThermalErosionSettings:
    iterations: int
    max_slope: float
    erosion_strength: float


def thermal_erosion(mesh: BMesh, settings: ThermalErosionSettings, erosion_status: ErosionStatus):
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

            for le in v.link_edges:
                le: BMEdge = le
                v_neigh = le.other_vert(v)
                # v_neigh = edge_get_neighbour_vertex(v, j)

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

            for le in v.link_edges:
                le: BMEdge = le
                v_neigh = le.other_vert(v)
                # v_neigh = edge_get_neighbour_vertex(v, j)

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

    erosion_status.is_running = False
