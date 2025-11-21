from htmlnode import LeafNode, ParentNode
from textnode import TextType, TextNode, BlockType
import os
import re
import shutil

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
def text_to_textnodes(text: str) -> list['TextNode']:
    initial_node = TextNode(text, TextType.TEXT)
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

def strip_markdown_prefix(block: str, block_type: 'BlockType') -> str:
    match block_type:
        case BlockType.PARAGRAPH:
            text = block.replace("\n", " ")
            return text
        case BlockType.HEADING:
            matches = re.match(r"#{1,6} ", block)
            prefix = matches.group(0)
            text = block[len(prefix):]
            return text
        case BlockType.QUOTE:
            lines = block.split("\n")
            stripped_lines = []
            for line in lines:
                stripped_lines.append(line[1:].lstrip())
            text = " ".join(stripped_lines)
            return text
        case BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            stripped_lines = []
            for line in lines:
                stripped_lines.append(line[2:])
            text = "\n".join(stripped_lines)
            return text
        case BlockType.ORDERED_LIST:
            lines = block.split("\n")
            stripped_lines = []
            for line in lines:
                idx = line.find(". ")
                stripped_lines.append(line[idx+2:])
            text = "\n".join(stripped_lines)
            return text
        case _:
            raise ValueError(f"Invalid block type: {block_type}")

def process_heading(block: str) -> int:
    matches = re.match(r"#{1,6} ", block)
    prefix = matches.group(0)
    level = prefix.count("#")
    return level

def process_code(block: str) -> 'ParentNode':
    first_newline = block.find('\n')
    last_newline = block.rfind('\n')
    inner = block[first_newline+1:last_newline+1]
    text_node = LeafNode(None, inner)
    code_node = ParentNode("code", [text_node])
    pre_node = ParentNode("pre", [code_node])
    return pre_node

def block_to_html(block: str, children: list['LeafNode'], block_type: 'BlockType') -> 'HTMLNode':
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode("p", children)
        case BlockType.HEADING:
            level = process_heading(block)
            return ParentNode(f"h{level}", children)
        case BlockType.QUOTE:
            return ParentNode("ol", children)
        case _:
            raise ValueError(f"Invalid block type: {block_type}")

def block_to_children(html_node_text: str) -> list['LeafNode']:
    children = []                                                       # initialize empty list
    text_nodes = text_to_textnodes(html_node_text)                      # convert the block text into inline text nodes
    for text_node in text_nodes:                                        # convert text nodes to html nodes and return them in a list as children
        children.append(text_node_to_html_node(text_node))
    return children

def list_items_to_children(block: str, block_type: 'BlockType') -> list['ParentNode']:
    # Strip the markdown prefix from each line
    stripped = strip_markdown_prefix(block, block_type)

    # Split into individual lines
    lines = stripped.split("\n")

    list_items = []
    for line in lines:
        children = block_to_children(line)
        node = ParentNode("li", children)
        list_items.append(node)

    return list_items

def markdown_to_html_node(markdown: str) -> 'ParentNode':
    nodes = []
    blocks = markdown_to_blocks(markdown)                               # split markdown into blocks
    for block in blocks:                                                # loop over each block
        block_type = block_to_block_type(block)                         # determine block type
        if block_type is BlockType.CODE:                                # special case for CODE - no children
            html_node = process_code(block)
            nodes.append(html_node)
            continue
        if block_type is BlockType.ORDERED_LIST or block_type is BlockType.UNORDERED_LIST:
            children = list_items_to_children(block, block_type)
            html_node = block_to_html(block, children, block_type)
            nodes.append(html_node)
            continue
        stripped = strip_markdown_prefix(block, block_type)
        children = block_to_children(stripped)                          # get child htmlnode objects from the block
        html_node = block_to_html(block, children, block_type)          # create parent html node
        nodes.append(html_node)

    return ParentNode("div", nodes)                                     # return the final HTML node

# COPY STATIC CONTENT
def copy_dir(src: str, dst: str) -> None:
    # list the contents of the src dir and iterate over them
    files = os.listdir(src)
    for file in files:
        # log the full path of the src and dst files
        file_path_src = os.path.join(src, file)
        file_path_dst = os.path.join(dst, file)

        # check if file is a regular file or directory - regular file -> copy, directory -> recurse
        if os.path.isfile(file_path_src):
            # copy src file to dst
            print(f"copying {file_path_src} to {file_path_dst}")
            shutil.copy(file_path_src, file_path_dst)
        elif os.path.isdir(file_path_src):
            # create the new dir at the destination if it does not exist already
            if not os.path.exists(file_path_dst):
                os.mkdir(file_path_dst)
            # recurse
            copy_dir(file_path_src, file_path_dst)
        else:
            print(f"File type not supported. The source file is neither a regular file nor directory.")

def copy_static_to_public(source: str, destination: str) -> None:
    src = f"{source}"
    dst = f"{destination}"
    # clean destination dir
    try:
        shutil.rmtree(dst)
        print(f'Directory "{dst}" deleted successfully.')
    except FileNotFoundError:
        pass

    # create dst dir
    os.mkdir(dst)

    # copy src content to dst
    copy_dir(src, dst)

