# utils.py

import numpy as np
import cv2
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
def imshow(image, title='', figure=True, cmap=None, figsize=None, show=True,
    axis='off'):
    if figure:
        if figsize == None:
            plt.figure()
        else:
            plt.figure(figsize=figsize)
    #
    if cmap=='gray':
        plt.imshow(image, cmap=cmap)
    else:
        plt.imshow(image)
    #
    if title:
        plt.title(title)
    plt.axis(axis)
    if show:
        plt.show()
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
def imread(filename, cmap='color'):
    if cmap=='gray':
        return cv2.imread(filename, 0)
    else:
        return cv2.imread(filename, 1)
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def is_square(image):
    h,w = image.shape[:2]
    if h == w:
        return True
    return False
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def cvt_square(image):
    h,w = image.shape[:2]
    if h > w:
        dif = int((h - w)/2)
        out_image = image[dif:dif + w, :]
        return out_image
    elif w > h:
        dif = int((w - h)/2)
        out_image = image[:, dif:dif + h]
        return out_image
    else:
        return image
# -----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
def resize_image(image, shape, interpolation='cubic'):
    #def resize_image(image, shape):
    resolution = shape[:2]
    if is_square(image):
        image = cvt_square(image)
    # -------------------------------------------------------------------------
    #
    if interpolation=='linear':
        inter = cv2.INTER_LINEAR
    elif interpolation=='cubic':
        inter = cv2.INTER_CUBIC
    else:
        inter = interpolation
    #
    # ------------------------------------------------------------------------
    rimg = cv2.resize(image, dsize=resolution, interpolation=inter)
    #rimg = cv2.resize(image, (590, 590), interpolation=cv2.INTER_CUBIC)
    return rimg
    #return cv2.resize(image, resolution)
# -----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
def resize_format(image, format):
    h_out, w_out =  format[:2]
    h_in, w_in = image.shape[:2]
    #
    # print(format)
    # print(image.shape)
    # jk = input()
    #
    if w_in/h_in > w_out/h_out:
        w = w_in * w_out // h_out
        image = crop_image(image, (0, h_in), ((w_in - w)//2, (3 * w_in - w)//2))
        #print('case 1')
    elif w_in/h_in < w_out/h_out:
        h = h_in * h_out // w_out
        image = crop_image(image, ((h_in - h)//2, (3 * h_in - h)//2), (0, w_in))
        #print('case 2')
    else:
        pass
        #print('case 3')
    out_image = resize_up_main_image(image, format[::-1])
    return out_image
# -----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
def crop_image(image, pt1 = (0,0), pt2=None):
    h1,w1 = pt1
    if pt2==None:
        pt2 = image.shape[:2]
    h2,w2 = pt2

    return image[h1:h2, w1:w2]
# -----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
def resize_up_main_image(image, resolution):
    resolution = resolution[:2]
    print(resolution)
    return cv2.resize(image, dsize=resolution, interpolation=cv2.INTER_CUBIC)
# -----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
def imwrite(filename, image):
    #print(filename)
    return cv2.imwrite(filename, image)
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def imgrotate(image, index):
    output = np.rot90(np.fliplr(image), index % 4) if (index // 4) else np.rot90(image, index % 4)
    return output
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def format_number(i):
    return '%04d'%(i)
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def format_percent(item):
    #fmt_str = '%' + '2.' + str(decimals) + 'f' #+ r'%' + ' '*4
    return '%2.2f'%(item)
    #return fmt_str%(item)
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def square_image(image, minishape):
    return resize_image(cvt_square(image), minishape, interpolation='cubic')
