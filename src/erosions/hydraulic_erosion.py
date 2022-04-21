import bpy
from bmesh.types import BMesh, BMVert
import numpy as np
from datetime import datetime

from .tools import edge_get_neighbour_vertex


class HydraulicErosionSettings:
    iterations: int
    rain_intensity: float
    soil_solubility: float
    evaporation_intensity: float
    sediment_capacity: float
    # Indices of selected vertices of vertex groups (if this option is selected)
    selected_vertex_indices: list[int] = None


# `ctrl+a -> scale` to apply scale transformation before calling this function
def hydraulic_erosion(mesh: BMesh, settings: HydraulicErosionSettings):
    start_time = datetime.now()

    mesh.verts.ensure_lookup_table()

    # # Constant amount of water that falls on a cell every iteration to simulate rain
    # K_r = 0.01
    # # Solubility constant of the terrain
    # K_s = 0.01
    # # Evaporation coefficient
    # K_e = 0.5
    # # Sediment capacity coefficient
    # K_c = 0.01

    # Constant amount of water that falls on a cell every iteration to simulate rain
    K_r = settings.rain_intensity
    # Solubility constant of the terrain
    K_s = settings.soil_solubility
    # Evaporation coefficient
    K_e = settings.evaporation_intensity / 100
    # Sediment capacity coefficient
    K_c = settings.sediment_capacity / 100

    # Water map
    w = np.zeros(len(mesh.verts), dtype=float)
    # Sediment map
    m = np.zeros(len(mesh.verts), dtype=float)

    iterations = settings.iterations

    # Iterations
    for _ in range(iterations):

        # Step 1
        # Rain fall
        if settings.selected_vertex_indices is None:
            w += K_r
        else:
            for index in settings.selected_vertex_indices:
                w[index] += K_r

        # Step 2
        # Erode material and convert it to sediment
        for i in range(len(mesh.verts)):
            v = mesh.verts[i]

            eroded_sediment = K_s * w[i]

            v.co.z -= eroded_sediment
            m[i] += eroded_sediment

        # Step 3
        # Distribute water and sediment

        # Amount of water to be moved to cell
        w_delta = np.zeros(w.size, dtype=float)
        # Amount of sediment to be moved to cell
        m_delta = np.zeros(m.size, dtype=float)

        # Water and sediment distribution
        for i in range(len(mesh.verts)):
            v = mesh.verts[i]

            # Total height of current cell (height + water)
            a = v.co.z + w[i]

            # Total delta of neighboring cells lower than current cell
            d_total = 0

            # Total height of all cells involved in the distribution (current cell including),
            # used for calculating average height of these cells
            a_total = 0
            # Count of values in `a_total` (for calculating average)
            a_count = 0

            # Count how many neighbour cells are lower than current cell and calculate their total delta and height
            for j in range(len(v.link_edges)):
                v_neigh = edge_get_neighbour_vertex(v, j)

                a_neigh = v_neigh.co.z + w[v_neigh.index]
                # Only lower cells are involved in the distribution
                if a_neigh < a:
                    d_total += a - a_neigh
                    a_total += a_neigh
                    a_count += 1

            # Current cell is also involved in the distribution
            a_total += a
            a_count += 1

            # Average height of cells involved in the distribution
            a_average = a_total / a_count

            # TODO: comment
            # TODO: "height delta that should be distributed to neighbouring cells if enough water is available" ?
            a_delta = a - a_average

            # Calculate water and sediment distribution
            for j in range(len(v.link_edges)):
                v_neigh = edge_get_neighbour_vertex(v, j)

                # Index of neighbour cell
                i_neigh = v_neigh.index

                a_neigh = v_neigh.co.z + w[i_neigh]
                # Only lower cells are involved in the distribution
                if a_neigh < a:
                    d = a - a_neigh

                    # Water distribution
                    water_delta = 0
                    if d_total != 0:
                        water_delta = min(w[i], a_delta) * (d / d_total)

                    w_delta[i_neigh] += water_delta
                    w_delta[i] -= water_delta

                    # Sediment distribution
                    sediment_delta = 0
                    if w[i] != 0:
                        sediment_delta = m[i] * (water_delta / w[i])

                    m_delta[i_neigh] += sediment_delta
                    m_delta[i] -= sediment_delta

        # Distribute water and sediment
        for i in range(len(mesh.verts)):
            w[i] += w_delta[i]
            # TODO: optimize by setting delta array values to 0 here instead of creating the whole array avery iteration
            # w_delta[i] = 0

            m[i] += m_delta[i]
            # m_delta[i] = 0

        # Step 4
        # Evaporation
        w *= 1 - K_e

        for i in range(len(mesh.verts)):
            v = mesh.verts[i]

            m_max = K_c * w[i]
            m_delta_2 = max(0, m[i] - m_max)

            m[i] -= m_delta_2
            v.co.z += m_delta_2

    for i in range(len(mesh.verts)):
        v = mesh.verts[i]

        v.co.z += m[i]
        m[i] = 0

    print(datetime.now() - start_time)
