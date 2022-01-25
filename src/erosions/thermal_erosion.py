from bmesh.types import BMesh
import numpy as np
from math import sqrt
from datetime import datetime
from .tools import edge_get_neighbour_vertex

# `ctrl+a -> scale` to apply scale transformation before calling this function
def thermal_erosion(mesh: BMesh):
    start_time = datetime.now()

    mesh.verts.ensure_lookup_table()

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
    T = 0.3
    C = 0.001

    iterations = 100

    for iteration in range(iterations):

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

    """ Debug """
    if True:
        temp_sum = 0
        for i in range(len(mesh.verts)):
            temp_sum += mesh.verts[i].co.z
        print(f"After = {temp_sum}")
    """ Debug end """

    print(datetime.now() - start_time)
