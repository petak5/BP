from bmesh.types import BMesh, BMVert, BMEdge
import numpy as np
from math import sqrt

from terrain_eroder.erosions.erosion_status import ErosionStatus


class ThermalErosionSettings:
    iterations: int
    max_slope: float
    erosion_strength: float


def thermal_erosion(mesh: BMesh, settings: ThermalErosionSettings, erosion_status: ErosionStatus):

    # Talus angle - slopes above this angle slide downhill
    T = settings.max_slope / 100
    # Erosion strength - determines how much material is moved
    C = settings.erosion_strength

    iterations = settings.iterations

    for iter in range(iterations):

        delta = np.zeros(len(mesh.verts), dtype=float)

        for i in range(len(mesh.verts)):
            v = mesh.verts[i]

            d_total = 0
            angle_max = 0

            # Values of d and angle are saved to avoid computing it twice
            ds = np.zeros(len(v.link_edges), dtype=float)
            angles = np.zeros(len(v.link_edges), dtype=float)

            i = 0
            for le in v.link_edges:
                le: BMEdge = le
                v_neigh = le.other_vert(v)

                # height delta
                d = v.co.z - v_neigh.co.z
                ds[i] = d

                xy_distance = sqrt(pow(v.co.x - v_neigh.co.x, 2) + pow(v.co.y - v_neigh.co.y, 2))
                if xy_distance == 0:
                    if d >= 0:
                        angle = 90
                    else:
                        angle = -90
                else:
                    angle = d / xy_distance
                angles[i] = angle

                if angle > T:
                    d_total += d

                    if angle > angle_max:
                        angle_max = angle
                i += 1

            # The difference of maximum angle from neighbouring cells and talus angle,
            # divided by 90 resulting in values from the range <0, 1>
            angle_diff_ratio = (angle_max - T) / 90

            i = 0
            for le in v.link_edges:
                le: BMEdge = le
                v_neigh = le.other_vert(v)

                # height delta
                d = ds[i]
                angle = angles[i]

                if angle > T:
                    # The ammount of soil to be moved
                    move_by = C * angle_diff_ratio * (d / d_total)

                    delta[v_neigh.index] += move_by
                    delta[v.index] -= move_by
                i += 1

        # Apply changes from erosion to the mesh
        for i in range(len(mesh.verts)):
            v = mesh.verts[i]

            v.co.z += delta[i]

        erosion_status.progress = round(100 * iter / iterations)
        if erosion_status.stop_requested:
            return

    erosion_status.is_running = False
