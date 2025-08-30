import os
import shutil
from file_utils import copy_contents, generate_page_recursive

DIR_PATH_STATIC = './static'
DIR_PATH_PUBLIC = './public'

DIR_PATH_CONTENT = "./content"
TEMPLATE_PATH = "./template.html"

def main():
    if os.path.exists(DIR_PATH_PUBLIC):
        print(f"Directory exists -> {DIR_PATH_PUBLIC}")
        print("Deleting public directory...")
        shutil.rmtree(DIR_PATH_PUBLIC)
    print("Copying static files to public directory...")
    copy_contents(DIR_PATH_STATIC, DIR_PATH_PUBLIC)

    print("Generating page...")
    generate_page_recursive(
        DIR_PATH_CONTENT,
        TEMPLATE_PATH,
        DIR_PATH_PUBLIC,
    )

if __name__ == "__main__":
    main()
