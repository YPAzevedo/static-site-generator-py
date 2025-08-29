class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        if value and children:
            raise ValueError("HTMLNode can't have value and children")
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        attr = ""

        if not self.props:
            return attr

        for prop in self.props.items():
            key, value = prop
            attr+=f" {key}=\"{value}\""

        return attr

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
