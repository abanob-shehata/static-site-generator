from os import listdir, mkdir
from os.path import exists, isfile
from shutil import rmtree, copy


path_stat = "./static"
path_pub = "./public"

def main():
    print("Deleting public directory...")
    if exists(path_pub):
        rmtree(path_pub)
    print("Copying static directory to public...")
    cp_static_to_public(path_stat, path_pub)
    return
    
def cp_static_to_public(src, dst):
    if exists(src):
        list = listdir(src)
        if not exists(dst):
            print(f"Creating directory {dst}")
            mkdir(dst)
        if list:
            for item in list:
                if isfile(src + "/" + item):
                    print(f"Copying {src}/{item} to {dst}/{item}")
                    copy(src + "/" + item, dst + "/" + item)
                else:
                    cp_static_to_public(src + "/" + item, dst + "/" + item)

main()