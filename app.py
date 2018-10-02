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
    generate_mosaic,
    correlation_matrix_resize,
    generate_mosaic_resize,
    create_photos
    )
from muralia.files import (
    files_from_dir,
    is_file_exist,
    join_path,
    mkdir,
    load_list,
    save_list,
    mk_all_dirs
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

    # folders
    set_path = 'set_images' # folder de imagenes pequenas # INPUT
    output_path = 'output_images' # folder donde se almancenan los archivos salida # INPUT
    __ = mk_all_dirs('output_images', root=True)

    # files
    main_image = 'main_images/jennifer.jpg' # imagen original # INPUT
    correlation_file = join_path(output_path,'correlation_file') # archivo de la matrix de correlacion
    path_output_filename_small = join_path(output_path,'path_output_filename_small.txt') # lista de miniarchivos
    output_path_mosaic = join_path(output_path,'mosaic_output.png') # mosaico
    path_output_main_image = join_path(output_path,'main_image/output_main.png') # salida output
    output_filenames_list_pos = join_path(output_path, 'filenames_and_positions.txt')
    output_photo_path = join_path(output_path, 'output_photo_path')

    # --------------------------------------------------------------------------
    # se escoge el tamano apropiado para las imagenes pequenas

    #little_shape = (590, 590, 3)
    little_shape = (32,32,3)
    shape_images = (36,64) #16:9

    #little_shape = (295, 295, 3)
    #shape_images = (36, 64) #16:9
    #shape_images = (28,21) #4:3
    #shape_images = (24,24) #1:1
    # --------------------------------------------------------------------------
    # se leen las imagenes pequenas
    if (is_file_exist(path_output_filename_small)):
        set_files = load_list(path_output_filename_small)
    else:
        set_files = files_from_dir(set_path, root=False)
        set_files.sort()
        save_list(path_output_filename_small, set_files)
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    #resize_files = files_from_dir(resize_path, root=True)
    #resize_files.sort()
    new_set_path = [join_path(set_path, item) for item in set_files]
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    if not is_file_exist(correlation_file + '.npz'):
        print('creating a correlation matrix and save... ')
        pos_list = list(range(8))
        corr_mat, pos_mat =  correlation_matrix_resize(main_image, path_output_main_image, new_set_path, little_shape, shape_images, pos_list)
        np.savez_compressed('output_images/correlation_file', a=corr_mat, b=pos_mat)
    else:
        print('load correlation matrix... ')
        loaded = np.load(correlation_file + '.npz')
        corr_mat = loaded['a']
        pos_mat = loaded['b']
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    generate_mosaic_resize(shape_images, corr_mat, new_set_path, pos_mat, little_shape, output_path_mosaic, output_filenames_list_pos)
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    create_photos(output_photo_path, output_filenames_list_pos)
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    print('success!')
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
