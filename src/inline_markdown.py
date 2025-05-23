import re
from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    newImagesNodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            newImagesNodes.append(node)
            continue

        originalText = node.text
        imgMatches = extract_markdown_images(node.text)

        if len(imgMatches) == 0:
            newImagesNodes.append(node)
            continue

        for match in imgMatches:
            img_alt = match[0]
            img_link = match[1]
            sections = originalText.split(f"![{img_alt}]({img_link})",1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                newImagesNodes.append(TextNode(sections[0], TextType.TEXT))

            newImagesNodes.append(TextNode(img_alt, TextType.IMAGE, img_link))

            originalText = sections[1]

        if originalText.strip() != "":
            newImagesNodes.append(TextNode(originalText, TextType.TEXT))

    return newImagesNodes


def split_nodes_link(old_nodes):
    newLinkNodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            newLinkNodes.append(node)
            continue
        originalText = node.text
        linkMatches = extract_markdown_links(originalText)
        if len(linkMatches) == 0:
            newLinkNodes.append(node)
            continue
        for match in linkMatches:
            link_alt = match[0]
            link = match[1]
            sections = originalText.split(f"[{link_alt}]({link})",1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                newLinkNodes.append(TextNode(sections[0], TextType.TEXT))

            newLinkNodes.append(TextNode(link_alt, TextType.LINK, link))
            originalText = sections[1]

        if originalText.strip() != "":
            newLinkNodes.append(TextNode(originalText, TextType.TEXT))

    return newLinkNodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes



