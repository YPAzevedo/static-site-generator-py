from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.children:
            raise ValueError("All ParentNodes must have children")
        if not self.tag:
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
