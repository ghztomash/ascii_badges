def bilinear_interpolation(x, y, arr):
    # Get the indices of the four corners
    x1, y1 = int(x), int(y)
    x2, y2 = min(x1 + 1, len(arr) - 1), min(y1 + 1, len(arr[0]) - 1)

    # Get the values at the four corners
    q11, q12, q21, q22 = arr[x1][y1], arr[x1][y2], arr[x2][y1], arr[x2][y2]

    # Perform linear interpolation in the x direction
    r1 = q11 * (1 - (x - x1)) + q21 * (x - x1)
    r2 = q12 * (1 - (x - x1)) + q22 * (x - x1)

    # Perform linear interpolation in the y direction
    interp = r1 * (1 - (y - y1)) + r2 * (y - y1)

    return interp

def resize_array(arr, new_shape):
    old_shape = [len(arr), len(arr[0])]
    new_arr = [[0 for _ in range(new_shape[1])] for _ in range(new_shape[0])]

    for i in range(new_shape[0]):
        for j in range(new_shape[1]):
            # Calculate the corresponding position in the old array
            x = (i / (new_shape[0] - 1)) * (old_shape[0] - 1) if new_shape[0] > 1 else 0
            y = (j / (new_shape[1] - 1)) * (old_shape[1] - 1) if new_shape[1] > 1 else 0
            # Perform bilinear interpolation at this position
            new_arr[i][j] = bilinear_interpolation(x, y, arr)

    return new_arr
