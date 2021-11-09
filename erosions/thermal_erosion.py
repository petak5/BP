from bmesh.types import BMesh


def basic_thermal_erosion(mesh: BMesh) -> BMesh:
    for v in mesh.verts:
        v.co.z += 1

    return mesh
