# pdi.py

import numpy as np
from scipy import signal
from muralia.utils import imread, resize_format, imshow, resize_image, imwrite
from muralia.files import is_file_exist, mkdir, join_path, files_from_dir
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
""" ------------------------------------------------------------------------ """
def compare_dist(img1, img2, log=True, dist='euclidean'):
    shape1 = np.prod(img1.shape)
    shape2 = np.prod(img2.shape)
    # validate shapes
    #print(img1.shape)
    #print(img2.shape)
    #jk = input()

    if (shape1 != shape2):
        print('imagenes must be same shape')
        return False
    # convert type
    img1 = img1.astype(np.int32).flatten()
    img2 = img2.astype(np.int32).flatten()
    """
    print('dimensiones imagen 1: ')
    print(img1.shape)
    print('dimensiones imagen 2: ')
    print(img2.shape)
    """
    # using euclidean or manthan distance
    if dist == 'euclidean':
        distance = np.sum(np.square(img1 - img2), dtype=np.float32)/shape1
    else:
        distance = np.sum(np.abs(img1 - img2))/shape1
    # apply log
    if log:
        distance = np.log(1 + distance)
    return distance
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
""" ------------------------------------------------------------------------ """
"""
def compare_correlation(image1, image2, mode="same"):
    shape1 = np.prod(image1.shape)
    shape2 = np.prod(image2.shape)
    # validate shapes
    if (shape1 != shape2):
        print('imagenes must be same shape')
        return False
    # compare
    # return signal.correlate3d(image1, image2)
    corr = 0
    for i in range(3):
        corr += signal.correlate2d(image1[:,:,i], image2[:,:,i], mode="same")
    return corr/3
"""
""" ------------------------------------------------------------------------ """
def correlation_matrix_iter(set_path, segmen_path):
    n = len(set_path)
    m = len(segmen_path)
    mat = np.zeros((m,n), dtype=np.float32)
    total = m * n
    for i in range(m):
        segmen_image = imread(segmen_path[i])
        for j in range(n):
            set_image = imread(set_path[j])
            #print(set_image.shape)
            #print(segmen_image.shape)
            #jk = input()
            mat[i,j] = compare_dist(set_image, segmen_image, log=True)
            print('creating correlation matrix... progress: ' +
                str(100*(i*m + j)/total) + '% ', end='\r')
    print('creating correlation matrix... progress: 100\%')
    return mat
""" ------------------------------------------------------------------------ """
""" ------------------------------------------------------------------------ """
def correlation_matrix(path_image, path_output_main_image, set_path, little_shape, format=(9,16)):
    # se lee la imagen principal
    print('reading main image')
    image = imread(path_image)
    print('creating new main image')
    if is_file_exist(path_output_main_image):
        output = imread(path_output_main_image)
        imwrite(path_output_main_image, output)
    else:
        main_size = (little_shape[0] * format[0], little_shape[1] * format[1])
        output = resize_format(image, main_size)
    #imshow(main_image)
    print('reshape main image')
    output = reshape_main_image(output, format, little_shape)
    n = len(set_path)
    print('create empty correlation matrix')
    mat_corr = np.zeros((n, format[0]*format[1]), dtype=np.float32)
    print('comparitions')
    n_elem = int(np.prod(little_shape))
    for i,filename in enumerate(set_path):
        mini_image = imread(filename)
        #mat_corr[i,:] = get_correlation(output, mini_image)
        distance = np.sum(np.square(output - mini_image.flatten().astype(np.float32)), dtype=np.float32, axis=1)/n_elem
        mat_corr[i,:] = np.log(1 + distance)
        print('creating correlation matrix... progress: ' +
            str(100*i/n) + '% ', end='\r')
    print('creating correlation matrix... progress: 100\%')
    return mat_corr
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
"""
def reshape_main_image(main_image, format, little_shape):
    # listas y variables utiles
    lsh, lsw = little_shape[:2]
    i = [e for sl in [format[1] * [k] for k in range(format[0])] for e in sl]
    i1 = [lsh * item for item in i]
    i2 = [lsh*(item + 1) for item in i]
    #
    j = format[0] * list(range(format[1]))
    j1 = [lsw*item for item in j]
    j2 = [lsw*(item + 1) for item in j]
    #
    k = list(range(format[0] * format[1]))
    # asignacion (espero que funcione)
    # new_main_image[k, :] = main_image[lsh * i:lsh * i2, lsw * j:lsw * j2]
    new_main_image[k, :] = main_image[i1:i2, j1:j2].flatten()

    # return
    return new_main_image
"""
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
""" ADVERTENCIA, ESTA FUNCION DEBE SER OPTIMIZADA """
def reshape_main_image(main_image, format, little_shape):
    cont = 0
    new_main_image = np.zeros((format[0]*format[1], np.prod(little_shape)), dtype=np.float32)
    #print(new_main_image.shape)
    n_little = format[0]
    for i in range(n_little):
        for j in range(format[1]):
            p1 = (little_shape[0] * i, little_shape[1] * j)
            p2 =(little_shape[0] * (i + 1), little_shape[1] * (j + 1))
            crop = main_image[p1[0]:p2[0],p1[1]:p2[1]]
            #
            #print(crop.shape)
            #print(new_main_image.shape)
            #
            #inp = input()
            new_main_image[cont, :] = crop.flatten()
            cont += 1
    return new_main_image

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def get_correlation(output, mini_image):
    #new_mini_image = mini_image.flatten().astype(np.float32)
    #print(new_mini_image.shape[0])
    distance = np.sum(np.square(output - mini_image.flatten().astype(np.float32)), dtype=np.float32, axis=1) /new_mini_image.shape[0]
    return np.log(1 + distance)
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def segments_main_image(path_image, output_path, little_shape,
    format=(9,16)):
    image = imread(path_image)
    main_size = (little_shape[0] * format[0], little_shape[1] * format[1])
    # print(main_size)
    # print(little_shape)
    # print(format)
    # print(image.shape)
    #jk = input()
    output = resize_format(image, main_size)
    # imshow(output)
    cont = 0
    n_little = format[0]
    for i in range(n_little):
        for j in range(format[1]):
            filename_out = (
                join_path(output_path, "image_" + format_number(cont)) +
                '.png'
                )
            if is_file_exist(filename_out):
                break
            p1 = (little_shape[0] * i, little_shape[1] * j)
            p2 =(little_shape[0] * (i + 1), little_shape[1] * (j + 1))
            crop = crop_image(output, p1, p2)
            # imshow(crop)
            # time.sleep(0.3)
            imwrite(filename_out, crop)
            cont += 1
        print('creating small images... progress: ' +
            str(int(100*(i+1)/n_little)) + '% ', end='\r')
    print('')
    pass
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def create_small_images(set_path, resize_path, little_shape, check=False):
    # ya se tienen los archivos, se varifican si existen en el path de salida
    # se crea un directorio donde guardar los archivos
    set_files = files_from_dir(set_path, root=False)
    mkdir(resize_path)
    n_little = len(set_files)
    # se recorren los archivo
    if check:
        for i,f in enumerate(set_files):
            fileout = join_path(resize_path, f)
            if not is_file_exist(fileout):
                #print('File not found, creating image...')
                limage = imread(join_path(set_path, f))
                #limage = imread(f)
                resize = resize_image(limage, little_shape[:2])
                #imshow(resize, axis='on')
                value = imwrite(join_path(resize_path, f), resize)
            else:
                limage = imread(fileout)
                if limage.shape != little_shape:
                    limage = imread(join_path(set_path, f))
                    #limage = imread(f)
                    resize = resize_image(limage, little_shape[:2])
                    #imshow(resize, axis='on')
                    value = imwrite(join_path(resize_path, f), resize)
            print('creating small images... progress: ' +
                str(int(100*(i+1)/n_little)) + '% ', end='\r')
    else:
        for i,f in enumerate(set_files):
            fileout = join_path(resize_path, f)
            if not is_file_exist(fileout):
                #print('File not found, creating image...')
                limage = imread(join_path(set_path, f))
                #limage = imread(f)
                resize = resize_image(limage, little_shape[:2])
                #imshow(resize, axis='on')
                value = imwrite(join_path(resize_path, f), resize)
            print('creating small images... progress: ' +
                str(int(100*(i+1)/n_little)) + '% ', end='\r')

    print('')
