from htmlnode import LeafNode
from textnode import TextType, TextNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid type: {text_node.text_type}")

def split_nodes_delimiter(
    old_nodes: list['TextNode'], delimiter: str, text_type: 'TextType'
) -> list['TextNode']:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue
        old_node_split = old_node.text.split(delimiter)
        if len(old_node_split) % 2 == 0:
            raise ValueError(f'Invalid Markdown syntax - missing closing "{delimiter}"')
        for index, value in enumerate(old_node_split):
            if value == "":
                continue
            if index % 2 != 0:
                new_nodes.append(TextNode(value, text_type))
            else:
                new_nodes.append(TextNode(value, TextType.TEXT))
    return new_nodes
