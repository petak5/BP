import bpy
import mathutils


class CreateTerrainOperator(bpy.types.Operator):
    bl_label = "Create Terrain"
    bl_idname = "object.create_terrain_operator"

    def execute(self, context):
        self.create_terrain(context)
        return {'FINISHED'}

    def create_terrain(self, context):
        new_mesh = bpy.data.meshes.new("MyMesh")
        new_obj = bpy.data.objects.new("NewObject", new_mesh)
        new_collection = bpy.data.collections.new("NewCollection")

        bpy.context.scene.collection.children.link(new_collection)
        new_collection.objects.link(new_obj)

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

        new_obj.my_obj_props.old_displacement = bump_intensity

        new_mesh.from_pydata(vertices, [], polygons)
