from os import listdir
from os import mkdir as mkd
from os.path import join, isfile, isdir

# ----------------------------------------------------------------------------
def files_from_dir(pathdir, root=True):
    if root:
        files = []
        for f in listdir(pathdir):
            fn = join(pathdir, f)
            if isfile(fn):
                files.append(fn)
        return files
    else:
        return [f for f in listdir(pathdir) if isfile(join(pathdir,f))]

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
