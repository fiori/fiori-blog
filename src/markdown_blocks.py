from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    newBlockList = []
    for b in blocks:
        if b != "":
            newBlockList.append(b.strip())

    return newBlockList


def block_to_block_type(block):
    lines = block.split("\n")

    if "#" in block[:6]:
        headingCount = block[:6].count("#")
        if block[headingCount] == " ":
            return BlockType.HEADING

    if len(lines) > 2 and (block[0:3] == "```" and block[-3:] == "```"):
        return BlockType.CODE

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1

        return BlockType.ORDERED_LIST


    return BlockType.PARAGRAPH



