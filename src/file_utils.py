from ntpath import isfile
import os
import shutil

from markdown import extract_title, markdown_to_html_node


def copy_contents(source, destination):
    source_path = source
    destination_path = destination
    print(f"source_path -> {source_path}")
    print(f"destination_path -> {destination_path}")
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)

    for item in os.listdir(source_path):
        item_source_path = os.path.join(source_path, item)
        print(f"item_source_path -> {item_source_path}")
        item_destination_path = os.path.join(destination_path, item)

        if os.path.isdir(item_source_path):
            copy_contents(item_source_path, item_destination_path)
        elif os.path.isfile(item_source_path):
            print(f"trying to copy file {item_source_path} to {item_destination_path}")
            shutil.copy(item_source_path, item_destination_path)

def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content):
        print(f"Trying to generate FILE for {dir_path_content} to {dest_dir_path}...")
        generate_page(dir_path_content, template_path, dest_dir_path)
        return

    print("Trying to get all content in directory...")
    for item in os.listdir(dir_path_content):
        item_dir_path_content = os.path.join(dir_path_content, item)
        item_dest_dir_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(item_dir_path_content) and item_dir_path_content.endswith(".md"):
            item_dest_dir_path = item_dest_dir_path.replace(".md", ".html")
        print(f"Trying to generate content for {item_dir_path_content} to {item_dest_dir_path}")
        generate_page_recursive(item_dir_path_content, template_path, item_dest_dir_path)
