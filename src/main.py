from textnode import TextNode,TextType
from functions import copy_static_to_public

def main():
    test_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(test_node)

    copy_static_to_public("static", "public")

if __name__ == "__main__":
    main()
