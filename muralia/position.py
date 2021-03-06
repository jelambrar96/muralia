# position.py

import numpy as np
#import matplotlib.pyplot as plt
from muralia.utils import (
    imshow
)

def spiral(shape, center=None):
    print(shape)
    distances = distances_to_center(shape, center=center)
    #print(distances)
    imshow(distances)
    index = index_spiral(distances)
    #print(index)
    imshow(np.zeros(shape))
    new_image = spimat(np.zeros(shape), index)
    return new_image

""" ------------------------------------------------------------------------ """
def distances_to_center(shape, center=None):
    h, w = shape[:2]
    hv, wv = np.meshgrid(np.arange(h), np.arange(w), sparse=False,  indexing='ij')
    if center==None:
        center = (h/2, w/2)
    distances = np.square(hv - center[0]) + np.square(wv - center[1])
    #print(distances.shape)
    return distances

""" ------------------------------------------------------------------------ """
def index_spiral(image, reverse=False):
    h, w = image.shape[:2]
    n = h * w
    hv, wv = np.meshgrid(np.arange(h), np.arange(w), sparse=False, indexing='ij')
    # redimention
    image = image.flatten()
    hv = hv.flatten()
    wv = wv.flatten()
    #
    index = np.zeros((n,3))
    # order and setting
    ind = np.lexsort((wv, hv, image))
    index[:,0], index[:,1], index[:,2] = image[ind], hv[ind], wv[ind]
    return index

""" ------------------------------------------------------------------------ """
def spimat(image, index):
    n = np.prod(image.shape[:2])
    new_image = np.zeros_like(image)
    array = np.arange(n)
    new_index = index.astype(np.int32)
    new_image[new_index[range(n), 1], new_index[range(n), 2]] = array[range(n)]
    return new_image

""" ------------------------------------------------------------------------ """
def distances_to_point(shape, center=None):
    distances = distances_to_center(shape, center=center)
    return index_spiral(distances)
