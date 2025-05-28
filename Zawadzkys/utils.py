import random

def split_list_into_random_chunks(lst, n):
    if n <= 0 or n > len(lst):
        raise ValueError("n must be between 1 and the length of the list")
    split_points = sorted(random.sample(range(1, len(lst)), n - 1))
    chunks = []
    prev = 0
    for point in split_points:
        chunks.append(lst[prev:point])
        prev = point
    chunks.append(lst[prev:])
    return chunks