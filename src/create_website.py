from os import listdir, mkdir, makedirs
from os.path import exists, isfile
from shutil import copy
from re import findall
from block_md_parser import markdown_to_html_node
from htmlnode import ParentNode

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
                    
def extract_title(markdown):
    h1s = findall(r"(?<!#)# (.*)", markdown)
    if len(h1s) == 0:
        raise Exception("No valid tiple for this markdown file")
    return h1s[0].strip()

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")
    with open(from_path) as f:
        contents = f.read()
    with open(template_path) as f:
        template = f.read()
    html_node = markdown_to_html_node(contents)
    html_str = html_node.to_html()
    title = extract_title(contents)
    outoput_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_str)
    dir = "/".join(dest_path.split("/")[:-1])
    if not exists(dir):
        makedirs(dir)
    with open(dest_path,"w") as f:
        f.write(outoput_html)
        
def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    list = listdir(dir_path_content)
    if len(list) == 0:
        return
    for item in list:
        if isfile(dir_path_content + "/" + item):
            if item[-2:] != "md":
                continue
            generate_page(dir_path_content + "/" + item, template_path, dest_dir_path + "/" + item[:-2] + "html")
        else:
            generate_page_recursive(dir_path_content + "/" + item, template_path, dest_dir_path + "/" + item)
