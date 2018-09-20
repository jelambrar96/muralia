import json

from os import listdir
from os import mkdir as mkd
from os.path import join, isfile, isdir


# ----------------------------------------------------------------------------
def files_from_dir(pathdir, root=True, image=True):
    if image:
        files = [item for item in listdir(pathdir) if is_image_format(item)]
    else:
        files = listdir(pathdir)

    if root:
        n_files = []
        for f in files:
            fn = join(pathdir, f)
            if isfile(fn):
                files.append(fn)
        return n_files
    else:
        return [f for f in files if isfile(join(pathdir,f))]


# ----------------------------------------------------------------------------
def is_image_format(filename):
    imgformats3 = ['.png', '.jpg', '.tif', '.gif']
    extention = filename[-4:]
    if extention in imgformats3:
        return True
    imgformats4 = ['.jpeg', '.tiff']
    extention = filename[-5:]
    if extention in imgformats4:
        return True
    return False

# ----------------------------------------------------------------------------
def is_file_exist(path):
    return isfile(path)

# ----------------------------------------------------------------------------
def join_path(*args):
    return join(*args)

# ----------------------------------------------------------------------------
def mkdir(path):
    if(isdir(path)):
        return True
    else:
        mkd(path)
        return True
# ----------------------------------------------------------------------------
def save_list(filename, mylist):
    with open(filename, 'w') as f:
        for s in mylist:
            f.write(str(s) + '\n')
# ----------------------------------------------------------------------------
def load_list(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f]
# ----------------------------------------------------------------------------
def mk_all_dirs(out_path, root=False):
    dirs = {
        'resize':'resize',
        'main_image':'main_image',
        'output_photo_path':'output_photo_path'
    }
    #mkdir(join_path(resize, main_image))
    mkdir(out_path)
    for k in dirs:
        h = join_path(out_path, dirs[k])
        mkdir(h)
        if root:
            dirs[k] = h
    return dirs
# ----------------------------------------------------------------------------
def cretare_json_features(filename, path_main_image, path_set_images,
    main_resoltution, format, mini_shape, list_files):
    data = {
        'main_image' : path_main_image,
        'set_images' : path_set_images,
        'main_resolution' : main_resoltution,
        'format': format,
        'mini_shape': mini_shape,
        'list_pos_files': list_files
    }
    #print(data)
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)
# ----------------------------------------------------------------------------
def load_features_from_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data
