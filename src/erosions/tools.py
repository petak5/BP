import numpy as np

from bmesh.types import BMesh, BMVert, BMEdge
from ..model.types import Mesh, INDEX_X, INDEX_Y, INDEX_Z


# Returns neighbour vertex from edge at index i
def edge_get_neighbour_vertex(v: BMVert, i: int) -> BMVert:
    """
    Get neighbour vertex of vertex v in i-th edge

    :param v: reference vertex
    :param i: i-th edge
    :return: neighbour vertex from i-th edge
    """
    if v.link_edges[i].verts[0] == v:
        return v.link_edges[i].verts[1]
    else:
        return v.link_edges[i].verts[0]


def bmesh_to_mesh(bmesh: BMesh) -> Mesh:
    mesh = Mesh(preallocate_size=len(bmesh.verts))

    bmvert: BMVert
    for bmvert in bmesh.verts:
        vert = mesh.add_vertex(bmvert.index, bmvert.co.x, bmvert.co.y, bmvert.co.z)

        le: BMEdge
        for le in bmvert.link_edges:
            bmvert_neigh = le.other_vert(bmvert)
            vert_neigh = mesh.add_vertex(bmvert_neigh.index, bmvert_neigh.co.x, bmvert_neigh.co.y, bmvert_neigh.co.z)
            if vert_neigh is not None:
                mesh.add_edge(vert[0], vert_neigh[0])

    mesh.finalize()
    # print(f"{len(bmesh.verts)} -- {mesh.vertices_count}")
    return mesh


# def bmesh_to_mesh(bmesh: BMesh) -> Mesh:
#     mesh = Mesh()

#     bmvert: BMVert
#     for bmvert in bmesh.verts:
#         vert = mesh.add_vertex(bmvert.index, bmvert.co.x, bmvert.co.y, bmvert.co.z)

#         le: BMEdge
#         for le in bmvert.link_edges:
#             bmvert_neigh = le.other_vert(bmvert)
#             vert_neigh = mesh.add_vertex(bmvert_neigh.index, bmvert_neigh.co.x, bmvert_neigh.co.y, bmvert_neigh.co.z)
#             if vert_neigh is not None:
#                 mesh.add_edge(vert, vert_neigh)

#     return mesh


def mesh_to_bmesh(mesh: Mesh, bmesh: BMesh):
    bmvert: BMVert
    for bmvert in bmesh.verts:
        i = np.where(mesh.vertices["bmesh_id"] == bmvert.index)[0][0]
        vert = mesh.vertices[i]

        # vert = mesh.vertices[bmvert.index]
        bmvert.co.x = vert[INDEX_X]
        bmvert.co.y = vert[INDEX_Y]
        bmvert.co.z = vert[INDEX_Z]
