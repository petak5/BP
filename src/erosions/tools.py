from bmesh.types import BMVert


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
