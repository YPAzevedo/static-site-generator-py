from enum import Enum
import re

from htmlnode import HTMLNode

# paragraph
# heading
# code
# quote
# unordered_list
# ordered_list
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    """Determine the type of markdown block based on its content"""

    # Heading: 1-6 # characters, followed by space and text
    if re.match(r'^#{1,6} .+', block):
        return BlockType.HEADING

    # Code block: starts and ends with 3 backticks
    if block.startswith("```") and block.endswith("```") and len(block) > 6:
        return BlockType.CODE

    # Quote block: every line starts with >
    lines = block.split('\n')
    if lines and all(line.startswith('>') for line in lines if line.strip()):
        return BlockType.QUOTE

    # Unordered list: every line starts with - followed by space
    if lines and all(line.startswith('- ') for line in lines if line.strip()):
        return BlockType.UNORDERED_LIST

    # Ordered list: lines start with number. space, incrementing from 1
    if _is_ordered_list(lines):
        return BlockType.ORDERED_LIST

    # Default: paragraph
    return BlockType.PARAGRAPH

def _is_ordered_list(lines):
    """Check if lines form a valid ordered list (1. 2. 3. etc.)"""
    non_empty_lines = [line for line in lines if line.strip()]
    if not non_empty_lines:
        return False

    expected_num = 1
    for line in non_empty_lines:
        if not re.match(rf'^{expected_num}\. ', line):
            return False
        expected_num += 1

    return True
