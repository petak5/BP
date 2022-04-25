from math import sqrt, pow
import numpy as np
from datetime import datetime
import random

from ..model.types import Mesh, INDEX_ID, INDEX_X, INDEX_Y, INDEX_Z, ErosionStatus


class HydraulicErosionPBSettings:
    rain_intensity: float
    drop_size: float
    drop_max_steps: int
    drop_evaporation_intensity: float
    erosion_strength: float
    # soil_solubility: float
    # sediment_capacity: float
    # Indices of selected vertices of vertex groups (if this option is selected)
    # selected_vertex_indices: list[int] = None


def hydraulic_erosion_pb(mesh: Mesh, settings: HydraulicErosionPBSettings, erosion_status: ErosionStatus) -> Mesh:
    """ Debug """
    if True:
        temp_sum = np.sum(mesh.vertices["z"])
        print(f"Before = {temp_sum}")
    """ Debug end """

    random.seed(datetime.now())

    drop_deceleration_intensity = 0.1
    drop_evaporation_intensity = settings.drop_evaporation_intensity
    erosion_strength = settings.erosion_strength

    drops_count = int(mesh.vertices_count * settings.rain_intensity)
    for i in range(drops_count):
        drop_size = settings.drop_size
        drop_sediment = 0.0
        drop_steps_remaining = settings.drop_max_steps
        drop_speed = 0.1
        drop_position = mesh.vertices[random.randint(0, mesh.vertices_count - 1)]

        for _ in range(drop_steps_remaining):
            neigh_ids = np.where(mesh.edges[drop_position[INDEX_ID], : ] == True)[0]
            # No neighbours => skip to next drop
            if len(neigh_ids) == 0:
                break

            lowest_neigh_id = neigh_ids[0]
            for k in neigh_ids:
                if mesh.vertices[k][INDEX_Z] < mesh.vertices[lowest_neigh_id][INDEX_Z]:
                    lowest_neigh_id = k

            # drop_speed += erosion_strength / drop_size
            height_delta = mesh.vertices[lowest_neigh_id][INDEX_Z] - drop_position[INDEX_Z]
            if height_delta < 0:
                # Move drop
                drop_position_old = drop_position
                drop_position = mesh.vertices[lowest_neigh_id]
                # print(height_delta)
                c = -height_delta/2 * drop_speed * drop_size
                # print(f"C={c}")
                c2 = c - drop_sediment
                # print(f"C2={c2}")
                drop_sediment += c2
                drop_position_old[INDEX_Z] -= c2
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
        drop_position[INDEX_Z] += drop_sediment

        erosion_status.progress = round(100 * i / drops_count)

        # Return if stop is requested
        if erosion_status.stop_requested:
            return
    erosion_status.is_running = False


    """ Debug """
    if True:
        temp_sum = np.sum(mesh.vertices["z"])
        print(f"After  = {temp_sum}")
    """ Debug end """