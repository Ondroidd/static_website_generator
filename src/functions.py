from htmlnode import LeafNode
from textnode import TextType, TextNode, BlockType
import re

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

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes: list['TextNode']) -> list['TextNode']:

    new_nodes = []

    for old_node in old_nodes:
        current_text = old_node.text
        images = extract_markdown_images(current_text)

        if not images:
            new_nodes.append(old_node)
            continue

        for image in images:
            image_alt, image_link = image
            current_text_split = current_text.split(f"![{image_alt}]({image_link})", 1)
            if current_text_split[0]:
                new_nodes.append(TextNode(current_text_split[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            current_text = current_text_split[1]

        if not current_text:
            continue
        new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list['TextNode']) -> list['TextNode']:
    
    new_nodes = []

    for old_node in old_nodes:
        current_text = old_node.text
        links = extract_markdown_links(current_text)

        if not links:
            new_nodes.append(old_node)
            continue

        for link in links:
            link_text, url = link
            current_text_split = current_text.split(f"[{link_text}]({url})", 1)
            if current_text_split[0]:
                new_nodes.append(TextNode(current_text_split[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            current_text = current_text_split[1]

        if not current_text:
            continue
        new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text: str) -> list['TextNode']:
    initial_node = TextNode(text, TextType.TEXT)
    bold_delimited = split_nodes_delimiter([initial_node], "**", TextType.BOLD)
    italic_delimited = split_nodes_delimiter(bold_delimited, "_", TextType.ITALIC)
    code_delimited = split_nodes_delimiter(italic_delimited, "`", TextType.CODE)
    link_delimited = split_nodes_link(code_delimited)
    final = split_nodes_image(link_delimited)
    return final

# BLOCK MARKDOWN FUNCTIONS
def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    final_blocks = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        final_blocks.append(block)

    return final_blocks

def block_to_block_type(markdown_block: str) -> 'BlockType':
    lines = markdown_block.split("\n")
    if re.match(r"#{1,6} ", markdown_block):
        return BlockType.HEADING
    elif len(lines) > 1 and markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    else:
        for i, line in enumerate(lines):
            num = i + 1
            if not line.startswith(f"{num}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
