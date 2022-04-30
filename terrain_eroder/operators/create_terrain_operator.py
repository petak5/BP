import bpy
import mathutils

from terrain_eroder.properties.terrain_properties import TerrainProperties


class CreateTerrainOperator(bpy.types.Operator):
    bl_label = "Create"
    bl_idname = "object.create_terrain_operator"
    bl_description = "Creates terrain with specified parameters"

    def execute(self, context):
        self.create_terrain(context)
        return {'FINISHED'}

    def create_terrain(self, context: bpy.types.Context):
        new_mesh: bpy.types.Mesh = bpy.data.meshes.new("Terrain Mesh")
        new_obj: bpy.types.Object = bpy.data.objects.new("Terrain", new_mesh)

        context.scene.collection.objects.link(new_obj)

        # Select the object
        new_obj.select_set(True)
        context.view_layer.objects.active = new_obj

        properties: TerrainProperties = context.scene.terrain_properties

        mathutils.noise.seed_set(properties.seed)

        vertices = []
        polygons = []

        size_x: int = properties.size_x
        size_y: int = properties.size_y
        noise_scale = properties.noise_scale
        step_x: float = properties.step_x
        step_y: float = properties.step_y

        pos_x_offset = size_x * step_x / 2
        pos_y_offset = size_y * step_y / 2

        random_x = mathutils.noise.random()
        random_y = mathutils.noise.random()

        noise_lambda = self.__get_noise_lambda(properties)

        v_x = random_x
        for i in range(size_x):
            v_y = random_y

            for j in range(size_y):
                v = mathutils.Vector((v_x, v_y, 0))
                z = noise_lambda(v)

                vertices.append([i * step_x - pos_x_offset, j * step_y - pos_y_offset, z])

                # Create face
                if i > 0 and j > 0:
                    offset = (i * size_y) + j
                    polygons.append([offset - size_y - 1, offset - size_y, offset, offset - 1])

                v_y += noise_scale
            v_x += noise_scale

        new_mesh.from_pydata(vertices, [], polygons)


    def __get_noise_lambda(self, properties: TerrainProperties):
        # Assign the values to properties, this way the lambdas are shorter
        h = properties.h
        lacunarity = properties.lacunarity
        octaves = properties.octaves
        offset = properties.offset
        gain = properties.gain
        hard = properties.hard
        noise_basis = properties.noise_basis
        amplitude_scale = properties.amplitude_scale
        frequency_scale = properties.frequency_scale
        distortion = properties.distortion
        noise_type_1 = properties.noise_type_1
        noise_type_2 = properties.noise_type_2

        # Default is CELL method
        noise_lambda = lambda vector: mathutils.noise.cell(vector)

        if properties.random_method == "FRACTAL":
            noise_lambda = lambda vector: mathutils.noise.fractal(vector, h, lacunarity, octaves, noise_basis=noise_basis)
        elif properties.random_method == "HETERO_TERRAIN":
            noise_lambda = lambda vector: mathutils.noise.hetero_terrain(vector, h, lacunarity, octaves, offset, noise_basis=noise_basis)
        elif properties.random_method == "HYBRID_MULTI_FRACTAL":
            noise_lambda = lambda vector: mathutils.noise.hybrid_multi_fractal(vector, h, lacunarity, octaves, offset, gain, noise_basis=noise_basis)
        elif properties.random_method == "MULTI_FRACTAL":
            noise_lambda = lambda vector: mathutils.noise.multi_fractal(vector, h, lacunarity, octaves, noise_basis=noise_basis)
        elif properties.random_method == "NOISE":
            noise_lambda = lambda vector: mathutils.noise.noise(vector, noise_basis=noise_basis)
        elif properties.random_method == "RIDGED_MULTI_FRACTAL":
            noise_lambda = lambda vector: mathutils.noise.ridged_multi_fractal(vector, h, lacunarity, octaves, offset, gain, noise_basis=noise_basis)
        elif properties.random_method == "TURBULENCE":
            noise_lambda = lambda vector: mathutils.noise.turbulence(vector, octaves, hard, noise_basis=noise_basis, amplitude_scale=amplitude_scale, frequency_scale=frequency_scale)
        elif properties.random_method == "VARIABLE_LACUNARITY":
            noise_lambda = lambda vector: mathutils.noise.variable_lacunarity(vector, distortion, noise_type1=noise_type_1, noise_type2=noise_type_2)

        return noise_lambda
