from textnode import TextNode,TextType
from functions import copy_static_to_public, generate_page

def main():

    copy_static_to_public("static", "public")

    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()
