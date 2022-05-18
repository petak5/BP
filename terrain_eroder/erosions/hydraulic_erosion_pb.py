from math import sqrt, pow
from bmesh.types import BMesh, BMVert, BMEdge
from datetime import datetime
import random

from terrain_eroder.erosions.erosion_status import ErosionStatus


class HydraulicErosionPBSettings:
    rain_intensity: float
    drop_size: float
    drop_max_steps: int
    drop_evaporation_intensity: float
    # erosion_strength: float
    # soil_solubility: float
    # sediment_capacity: float
    # Indices of selected vertices of vertex groups (if this option is selected)
    # selected_vertex_indices: list[int] = None


def hydraulic_erosion_pb(mesh: BMesh, settings: HydraulicErosionPBSettings, erosion_status: ErosionStatus):
    random.seed(datetime.now())

    drop_deceleration_intensity = 0.1
    drop_evaporation_intensity = settings.drop_evaporation_intensity
    # erosion_strength = settings.erosion_strength

    drops_count = int(len(mesh.verts) * settings.rain_intensity)
    for i in range(drops_count):
        drop_size = settings.drop_size
        drop_sediment = 0.0
        drop_steps_remaining = settings.drop_max_steps
        drop_speed = 0.1
        drop_position = mesh.verts[random.randint(0, len(mesh.verts) - 1)]

        for _ in range(drop_steps_remaining):
            # No neighbours => skip to next drop
            if len(drop_position.link_edges) == 0:
                break

            lowest_neigh = drop_position.link_edges[0].other_vert(drop_position)
            for le in drop_position.link_edges:
                le: BMEdge = le
                v_neigh = le.other_vert(drop_position)
                if v_neigh.co.z < lowest_neigh.co.z:
                    lowest_neigh = v_neigh

            # drop_speed += erosion_strength / drop_size
            height_delta = lowest_neigh.co.z - drop_position.co.z
            if height_delta < 0:
                # Move drop
                drop_position_old = drop_position
                drop_position = lowest_neigh

                c = -height_delta/2 * drop_speed * drop_size

                c2 = c - drop_sediment

                drop_sediment += c2
                drop_position_old.co.z -= c2
            # else:
            #     # Try to fill the hole (current point is lower than all neighbours)
            #     deposit = min(height_delta, drop_sediment)
            #     # print(f"Deposit: {deposit}")
            #     drop_position[INDEX_Z] -= deposit
            #     drop_sediment          += deposit

            drop_size *= 1 - drop_evaporation_intensity
            # drop_speed *= 1 - drop_deceleration_intensity
            # drop_speed = sqrt(pow(drop_speed, 2) + abs(height_delta) * 10)
            if height_delta > 0:
                drop_speed += height_delta * 10

        # Deposit remaining sediment
        drop_position.co.z += drop_sediment

        erosion_status.progress = round(100 * i / drops_count)

        # Return if stop is requested
        if erosion_status.stop_requested:
            return
    erosion_status.is_running = False
