import numpy as np
from tqdm import tqdm
import cv2
    

def add_color(disp):
    disp = cv2.normalize(disp, None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    disp = (disp*255).astype(np.uint8)
    return cv2.applyColorMap(disp, cv2.COLORMAP_MAGMA)
    
  
def cal_disparity(imgL, imgR, blockSize):
    h, w = imgL.shape
    disparity_map = np.zeros((h, w))
    search_block_size = int(h/8)
    print(search_block_size)
    for y in tqdm(range(blockSize, h-blockSize)):
        for x in range(blockSize, w-blockSize):
            block_left = imgL[y:y + blockSize, x:x + blockSize]
            min_index = compare_blocks(y, x, block_left, imgR, search_block_size, block_size=blockSize)
            disparity_map[y, x] = abs(min_index[1] - x)
    return disparity_map

def sum_of_abs_diff(pixel_vals_1, pixel_vals_2):
    """
    Args:
        pixel_vals_1 (numpy.ndarray): pixel block from left image
        pixel_vals_2 (numpy.ndarray): pixel block from right image

    Returns:
        float: Sum of absolute difference between individual pixels
    """
    if pixel_vals_1.shape != pixel_vals_2.shape:
        return -1

    return np.sum(abs(pixel_vals_1 - pixel_vals_2))
    

def compare_blocks(y, x, block_left, right_array, search_block_size, block_size):
    """
    Compare left block of pixels with multiple blocks from the right
    image using SEARCH_BLOCK_SIZE to constrain the search in the right
    image.

    Args:
        y (int): row index of the left block
        x (int): column index of the left block
        block_left (numpy.ndarray): containing pixel values within the
                    block selected from the left image
        right_array (numpy.ndarray]): containing pixel values for the
                     entrire right image
        block_size (int, optional): Block of pixels width and height.
                                    Defaults to 5.

    Returns:
        tuple: (y, x) row and column index of the best matching block
                in the right image
    """
    # Get search range for the right image
    x_min = max(0, x)
    x_max = min(right_array.shape[1], x + search_block_size)
    #print(f'search bounding box: ({y, x_min}, ({y, x_max}))')
    first = True
    min_sad = None
    min_index = None
    for x in range(x_min, x_max):
        block_right = right_array[y: y+block_size,
                                  x: x+block_size]
        sad = sum_of_abs_diff(block_left, block_right)
        #print(f'sad: {sad}, {y, x}')
        if first:
            min_sad = sad
            min_index = (y, x)
            first = False
        else:
            if sad < min_sad:
                min_sad = sad
                min_index = (y, x)

    return min_index
