from enum import Enum
from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.children is None:
            raise ValueError("All ParentNodes must have children")
        if self.tag is None:
            raise ValueError("All ParentNodes must have a tag")
        
        children_html = ""

        for child in self.children:
            children_html+=child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    def get_children_html(self, child):
        if isinstance(child, LeafNode):
            return child.to_html()

        html = ""
        if isinstance(child, ParentNode):
            for c in child.children:
                html+=self.get_children_html(c)
        
        return html


    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
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
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH