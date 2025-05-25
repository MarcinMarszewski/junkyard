class PhongModel:
    def __init__(self, ambient_color, diffuse_color, specular_color, shininess):
        self.ambient_color = ambient_color
        self.diffuse_color = diffuse_color
        self.specular_color = specular_color
        self.shininess = shininess

    def calculate_ambient(self, light_intensity):
        return [light_intensity[i] * self.ambient_color[i] for i in range(3)]

    def calculate_diffuse(self, light_intensity, normal, light_direction):
        normal = normalize(normal)
        light_direction = normalize(light_direction)
        dot_product = max(dot_product(normal, light_direction), 0)
        return [light_intensity[i] * self.diffuse_color[i] * dot_product for i in range(3)]

    def calculate_specular(self, light_intensity, view_direction, normal, light_direction):
        normal = normalize(normal)
        light_direction = normalize(light_direction)
        reflect_direction = [2 * dot_product(normal, light_direction) * normal[i] - light_direction[i] for i in range(3)]
        reflect_direction = normalize(reflect_direction)
        dot_product = max(dot_product(reflect_direction, view_direction), 0)
        return [light_intensity[i] * self.specular_color[i] * (dot_product ** self.shininess) for i in range(3)]