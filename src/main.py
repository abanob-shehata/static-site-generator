from os.path import exists
from shutil import rmtree
from create_website import cp_static_to_public, generate_page

path_stat = "./static"
path_pub = "./public"

def main():
    print("Deleting public directory...")
    if exists(path_pub):
        rmtree(path_pub)
    print("Copying static directory to public...")
    cp_static_to_public(path_stat, path_pub)
    
    generate_page("content/index.md", "template.html", "public/index.html")
    return

main()