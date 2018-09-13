#!venv/bin/python3
#main.py
import numpy as np
import cv2
import time
#
from muralia.utils import (
    imread,
    imshow,
    imwrite,
    resize_image,
    resize_format,
    crop_image
    )
from muralia.pdi import (
    compare_dist,
    correlation_matrix,
    create_small_images,
    generate_mosaic
    )
from muralia.files import (
    files_from_dir,
    is_file_exist,
    join_path,
    mkdir,
    load_list,
    save_list
    )
from muralia.position import(
    distances_to_point
)
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def format_number(i):
    return '%04d'%(i)
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def main():
    set_path = 'set_images'
    resize_path = 'output_images/resize'
    main_image = 'main_images/jennifer.jpg'
    segments_path = 'output_images/segments'
    correlation_file = 'output_images/correlation_file'
    path_output_main_image = 'output_images/main_image/output_main.png'
    path_output_filename_small = 'output_images/path_output_filename_small.txt'
    output_path_mosaic = 'output_images/mosac_output.png'
    # --------------------------------------------------------------------------
    # se escoge el tamano apropiado para las imagenes pequenas

    #little_shape = (590, 590, 3)
    little_shape = (32,32,3)
    shape_images = (18,32) #16:9

    #little_shape = (295, 295, 3)
    #shape_images = (36, 64) #16:9

    #"""
    #shape_images = (28,21) #4:3
    #"""
    #"""
    #shape_images = (24,24) #1:1
    #"""
    # --------------------------------------------------------------------------
    # se leen las imagenes pequenas
    if (is_file_exist(path_output_filename_small)):
        set_files = load_list(path_output_filename_small)
    else:
        set_files = files_from_dir(set_path, root=False)
        set_files.sort()
        save_list(path_output_filename_small, set_files)
    """
    set_files = files_from_dir(set_path, root=False)
    set_files.sort()
    n_little = len(set_files)
    for f in set_files: print(f)
    """
    # --------------------------------------------------------------------------
    create_small_images(set_path, resize_path, little_shape)
    # --------------------------------------------------------------------------
    # segments_main_image(main_image, segments_path, little_shape, shape_images)
    #segments_files = files_from_dir(segments_path, root=True)
    #segments_files.sort()
    # --------------------------------------------------------------------------
    resize_files = files_from_dir(resize_path, root=True)
    resize_files.sort()
    # --------------------------------------------------------------------------
    if not is_file_exist(correlation_file + '.npz'):
        print('creating a correlation matrix and save... ')
        pos_list = list(range(8))
        corr_mat, pos_mat =  correlation_matrix(main_image, path_output_main_image, resize_files, little_shape, shape_images, pos_list)
        np.savez_compressed('output_images/correlation_file', a=corr_mat, b=pos_mat)
    else:
        print('load correlation matrix... ')
        loaded = np.load(correlation_file + '.npz')
        corr_mat = loaded['a']
        pos_mat = loaded['b']

    #print(corr_mat.shape)
    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    #index = [ (int(i),int(j)) for d,i,j in distances_to_point(shape_images)]
    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    new_set_files = [join_path(resize_path, item) for item in set_files]
    generate_mosaic(shape_images, corr_mat, new_set_files, pos_mat, little_shape, output_path_mosaic)

    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------

    print('success!')
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
