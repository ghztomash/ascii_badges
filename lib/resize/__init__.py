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

def resize_array(arr, new_shape, new_arr):
    old_shape = [len(arr), len(arr[0])]
    for i in range(new_shape[0]):
        for j in range(new_shape[1]):
            # Calculate the corresponding position in the old array
            x = (i / (new_shape[0] - 1)) * (old_shape[0] - 1) if new_shape[0] > 1 else 0
            y = (j / (new_shape[1] - 1)) * (old_shape[1] - 1) if new_shape[1] > 1 else 0
            # Perform bilinear interpolation at this position
            new_arr[i][j] = bilinear_interpolation(x, y, arr)


def bilinear_interpolation_1d(x, y, arr, width):
    # Get the indices of the four corners
    x1, y1 = int(x), int(y)
    x2, y2 = min(x1 + 1, len(arr) // width - 1), min(y1 + 1, width - 1)

    # Convert 2D indices to 1D indices
    i11, i12, i21, i22 = (
        x1 * width + y1,
        x1 * width + y2,
        x2 * width + y1,
        x2 * width + y2,
    )

    # Get the values at the four corners
    q11, q12, q21, q22 = arr[i11], arr[i12], arr[i21], arr[i22]

    # Perform linear interpolation in the x direction
    r1 = q11 * (1 - (x - x1)) + q21 * (x - x1)
    r2 = q12 * (1 - (x - x1)) + q22 * (x - x1)

    # Perform linear interpolation in the y direction
    interp = r1 * (1 - (y - y1)) + r2 * (y - y1)

    return int(interp)


def resize_array_1d(new_arr, new_width, old_arr, old_width):
    new_height = len(new_arr) // new_width
    old_height = len(old_arr) // old_width
    for k in range(new_width * new_height):
        i = k // new_width
        j = k % new_width
        # Calculate the corresponding position in the old array
        x = (i / (new_height - 1)) * (old_height - 1) if new_height > 1 else 0
        y = (j / (new_width - 1)) * (old_width - 1) if new_width > 1 else 0
        # Perform bilinear interpolation at this position
        new_arr[i * new_width + j] = bilinear_interpolation_1d(x, y, old_arr, old_width)

