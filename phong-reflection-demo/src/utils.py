def normalize(vector):
    length = (vector[0]**2 + vector[1]**2 + vector[2]**2) ** 0.5
    if length == 0:
        return vector
    return [component / length for component in vector]

def dot_product(v1, v2):
    return sum(a * b for a, b in zip(v1, v2))

def cross_product(v1, v2):
    return [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ]