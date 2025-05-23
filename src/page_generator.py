import os

from helpers import markdown_to_html_node

def generate_page(from_path, template_path, dest_path, base_path = "/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # read the markdown file from_path and store the contents in a variable

    mdFile = open(from_path, mode='r')
    mdFileContent = mdFile.read()
    mdFile.close()

    templateFile = open(template_path, mode='r')
    templateContent = templateFile.read()
    templateFile.close()


    htmlNodes = markdown_to_html_node(mdFileContent)
    htmlContent = htmlNodes.to_html()

    title = extract_title(mdFileContent)
    templateContent = templateContent.replace("{{ Title }}", title)
    templateContent = templateContent.replace("{{ Content }}", htmlContent)

    templateContent = templateContent.replace("href=\"/", f"href=\"{base_path}")
    templateContent = templateContent.replace("src=\"/", f"src=\"{base_path}")


    # generate the file
    filePaths = from_path.split("/")
    fileName = filePaths[-1].replace(".md",".html")
    fileToSavePath = os.path.join(dest_path, fileName)

    dest_dir_path = os.path.dirname(fileToSavePath)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    fileToSave = open(fileToSavePath, 'w')
    fileToSave.write(templateContent)
    fileToSave.close()
    print(f"Successfully created a file at {fileToSavePath}")



def extract_title(markdown:str):
    blocks = markdown.split("\n")
    for block in blocks:
        if block.startswith("# "):
             return block[2:].strip()


    raise ValueError("no title found")


