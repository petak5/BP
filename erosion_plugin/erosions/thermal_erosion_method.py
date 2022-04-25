import numpy as np
from math import sqrt

from ..model.types import Mesh, INDEX_ID, INDEX_X, INDEX_Y, INDEX_Z


def calculate_erosion(mesh: Mesh, T: float, C: float) -> dict[int, float]:
    # deltas: dict[int, float] = {}   # {vertex_id, height_change}
    deltas = np.zeros(shape=mesh.vertices.shape, dtype=float)

    # Initialize dictionary with zeros
    # deltas[vert.id] = 0
    # for vert_neigh in vert.neighbours:
    #     deltas[vert_neigh.id] = 0

    # vert: Vertex
    for vert in mesh.vertices:
        d_total = 0
        d_max = 0
        angle_max = 0

        neighbour_ids = np.where(mesh.edges[vert[INDEX_ID]] == True)[0]
        # print(neighbour_ids)

        for neigh_id in neighbour_ids:
            vert_neigh = mesh.vertices[neigh_id]
            # height delta
            d = vert[INDEX_Z] - vert_neigh[INDEX_Z]
            xy_distance = sqrt(pow(vert[INDEX_X] - vert_neigh[INDEX_X], 2) + pow(vert[INDEX_Y] - vert_neigh[INDEX_Y], 2))
            # if xy_distance == 0:
            #     print(f"({vert.id}) {vert.x} | {vert.y} : ({vert_neigh.id}) {vert_neigh.x} | {vert_neigh.y}\n\n")
            angle = d / xy_distance

            if angle > T:
                d_total += d

                if angle > angle_max:
                    angle_max = angle
                if d > d_max:
                    d_max = d

        for neigh_id in neighbour_ids:
            vert_neigh = mesh.vertices[neigh_id]

            # height delta
            d = vert[INDEX_Z] - vert_neigh[INDEX_Z]
            xy_distance = sqrt(pow(vert[INDEX_X] - vert_neigh[INDEX_X], 2) + pow(vert[INDEX_Y] - vert_neigh[INDEX_Y], 2))
            angle = d / xy_distance

            if angle > T:
                # move_by = C * (d_max - T) * (d / d_total)
                move_by = angle * C * (d / d_total)

                deltas[vert_neigh[INDEX_ID]] += move_by
                deltas[vert[INDEX_ID]] -= move_by

    return deltas
