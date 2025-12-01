from textnode import TextNode,TextType
from functions import copy_static_to_public, generate_pages_recursive
import sys

def main():

    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]

    copy_static_to_public("static", "docs")

    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()
