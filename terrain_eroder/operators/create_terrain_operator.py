import bpy
import mathutils


class CreateTerrainOperator(bpy.types.Operator):
    bl_label = "Create"
    bl_idname = "object.create_terrain_operator"
    bl_description = "Creates terrain with specified parameters"

    def execute(self, context):
        self.create_terrain(context)
        return {'FINISHED'}

    def create_terrain(self, context: bpy.types.Context):
        new_mesh = bpy.data.meshes.new("New Terrain Mesh")
        new_obj = bpy.data.objects.new("New Terrain", new_mesh)

        context.scene.collection.objects.link(new_obj)

        vertices = []
        polygons = []

        bump_intensity = 1
        grid_size = 61
        step_size = 0.05

        for i in range(0, grid_size, 1):
            for j in range(0, grid_size, 1):
                v_1 = mathutils.Vector((i/20.0, j/20.0, 0.0))
                v_2 = mathutils.Vector((i / 3.0, j / 3.0, 0.0))
                x_1 = mathutils.noise.fractal(v_1, 0.4, 1.0, 1, noise_basis="VORONOI_F1")
                x_2 = mathutils.noise.fractal(v_2, 0.4, 1.0, 1, noise_basis="PERLIN_NEW")
                ratio = 0.8
                x = x_1 * ratio + x_2 * (1 - ratio)
                vertices.append([i * step_size, j * step_size, x * bump_intensity])

                if i > 0 and j > 0:
                    offset = (i * grid_size) + j
                    # print(f"i = {i}, j = {j}, offset = {offset}")
                    polygons.append([offset - grid_size - 1, offset - 1, offset - grid_size])
                    polygons.append([offset - 1, offset - grid_size, offset])

        new_mesh.from_pydata(vertices, [], polygons)
