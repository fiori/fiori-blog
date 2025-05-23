from htmlnode import HTMLNode, LeafNode, ParentNode
import htmlnode
from inline_markdown import text_to_textnodes
from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks
from textnode import TextNode, TextType, text_node_to_html_node


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)

    return ParentNode("div", children)

def block_to_html_node(block):
    type = block_to_block_type(block)

    match type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return ulist_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return olist_to_html_node(block)

def code_to_html_node(block):
    raw_text_node = TextNode(block[4:-3], TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    return ParentNode("pre", [ParentNode("code", [child])])

def olist_to_html_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        children = text_to_children(line[3:])
        item = ParentNode("li", children)
        items.append(item)
    return ParentNode("ol", items)


def ulist_to_html_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        leaftNodes = text_to_children(line[2:])
        item = ParentNode("li", leaftNodes)
        items.append(item)
    return ParentNode("ul", items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def paragraph_to_html_node(block):
    paragraph = block.replace("\n", " ")
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = block[:6].count("#")
    children = text_to_children(block[level:].strip())
    return ParentNode(f"h{level}", children)

def text_to_children(text):
    textNodes = text_to_textnodes(text)
    children = []
    for tn in textNodes:
        children.append(text_node_to_html_node(tn))

    return children
