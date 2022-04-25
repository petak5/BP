import numpy as np

# Indices for the data type used to represend Vertex (it's just a tuple)
INDEX_ID = 0
INDEX_BMESH_ID = 1
INDEX_X = 2
INDEX_Y = 3
INDEX_Z = 4


class Mesh:
    vertex_data_type: np.dtype = np.dtype([("id", int), ("bmesh_id", int), ("x", float), ("y", float), ("z", float)])
    vertices: np.ndarray
    edges: np.ndarray
    vertices_count: int
    vertices_alloc_size: int
    edges_count = 0


    def __init__(self, preallocate_size: int = 0):
        self.vertices_count = 0
        if preallocate_size < 1:
            self.vertices_alloc_size = 2
        else:
            self.vertices_alloc_size = preallocate_size
        self.vertices = np.zeros(shape=(self.vertices_alloc_size), dtype=self.vertex_data_type)
        self.edges = np.zeros(shape=(self.vertices_alloc_size, self.vertices_alloc_size), dtype=bool)


    def add_vertex(self, bmesh_id: int, x: float, y: float, z: float) -> vertex_data_type:
        vertex: self.vertex_data_type

        # Check if vertex is not already in mesh
        temp1 = self.vertices[0:self.vertices_count]
        temp2 = temp1[temp1["bmesh_id"] == bmesh_id]
        if temp2.size == 0:
            if self.vertices_count == self.vertices_alloc_size:
                self.vertices_alloc_size *= 2
                self.vertices = np.resize(self.vertices, self.vertices_alloc_size)
                # self.edges =    np.resize(self.edges,   (self.vertices_alloc_size, self.vertices_alloc_size) )
                # self.edges.resize((self.vertices_alloc_size, self.vertices_alloc_size))
                old_edges = self.edges
                self.edges = np.zeros(shape=(self.vertices_alloc_size, self.vertices_alloc_size), dtype=bool)
                for i in range(old_edges.shape[0]):
                    for j in range(old_edges.shape[1]):
                        self.edges[i, j] = old_edges[i, j]
            vertex = (self.vertices_count, bmesh_id, x, y, z)
            self.vertices[self.vertices_count] = vertex
            self.vertices_count += 1
        else:
            vertex = temp2[0]

        return vertex


    def add_edge(self, vertex1: int, vertex2: int):
        self.edges[vertex1, vertex2] = True
        self.edges[vertex2, vertex1] = True
        self.edges_count += 1


    def finalize(self):
        if self.vertices_alloc_size != self.vertices_count:
            self.vertices_alloc_size = self.vertices_count
            self.vertices = np.resize(self.vertices, self.vertices_alloc_size)
            self.edges    = np.resize(self.edges,   (self.vertices_alloc_size, self.vertices_alloc_size))

        # TODO: No need for this anymore? I fixed it by always creating new empty 2D array and copying values from the old one.
        # TODO: What's the REAL reason? Isn't it odd that I have to set only the diagonal values to False? Isn't it needed for other items in the whole 2D array?
        # When resizing this 2D array of bools, it does not set the new values to False (the desired default)
        # np.fill_diagonal(self.edges, False)


class ErosionStatus:
    is_running: bool
    # signalize that the erosion (usually in other thread) should stop
    stop_requested: bool = False
    progress: int


    def __init__(self, is_running: bool = False, progress: int = 0):
        self.is_running = is_running
        self.progress = progress
