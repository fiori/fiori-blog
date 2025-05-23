import os
import shutil

def copy_src_to_dest(src, dest):
    srcExist = os.path.exists(src)

    if not srcExist:
        raise FileNotFoundError(f"Aquii {src} path does not exists")

    if not os.path.exists(dest):
        os.mkdir(dest)

    # copy all files and subdirectories, nestedfiles, etc
    for filename in os.listdir(src):
        path = os.path.join(src, filename)
        dstPath = os.path.join(dest, filename)
        if os.path.isfile(path):
            shutil.copy(path, dstPath)
            print(f"copy {path} to {dstPath}")
        else:
            copy_src_to_dest(path, dstPath)

