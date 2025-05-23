import sys
import os
import shutil

from copystatic import copy_src_to_dest
from page_generator import generate_page


dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content= "./content"
template_path = "./template.html"

def main():
    base_path = "/"
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    print(f"Baseee Path {base_path}")
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)


    print("Copying static files to public directory...")
    copy_src_to_dest(dir_path_static, dir_path_public)

    generate_pages_recursive(dir_path_content, template_path, dir_path_public, base_path)



def generate_pages_recursive(dir_path_from, template_path, dir_path_to, base_path = "/"):
    pagesToGenerate = os.listdir(dir_path_from)
    print(f"Pages To Generate : {pagesToGenerate}")
    for page in pagesToGenerate:
        pathToGenerate = os.path.join(dir_path_from, page)
        if os.path.isfile(pathToGenerate):
            generate_page(pathToGenerate, template_path, dir_path_to, base_path)
        else:
            dirPathDest = os.path.join(dir_path_to, page)
            generate_pages_recursive(pathToGenerate, template_path, dirPathDest, base_path)


if __name__ == "__main__":
    main()
