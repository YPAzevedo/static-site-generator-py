import unittest

from textnode import TextNode, TextType, text_node_to_html_node

TEST_URL = "https://www.example.com"

class TestTextNode(unittest.TestCase):
    def test_sets_all_properties(self):
        node = TextNode(text="test", text_type=TextType.LINK, url=TEST_URL)
        self.assertIsNotNone(node.text)
        self.assertIsNotNone(node.text_type)
        self.assertIsNotNone(node.url)

    def test_eq(self):
        node_a = TextNode(text="This is a text node", text_type=TextType.BOLD, url=None)
        node_b = TextNode(text="This is a text node", text_type=TextType.BOLD, url=None)
        self.assertEqual(node_a, node_b)

    def test_different_types(self):
        node_a = TextNode(text="This is a text node", text_type=TextType.LINK, url=None)
        node_b = TextNode(text="This is a text node", text_type=TextType.BOLD, url=None)
        self.assertNotEqual(node_a, node_b)

    def test_missing_link(self):
        node_a = TextNode(text="This is a text node", text_type=TextType.LINK, url=None)
        node_b = TextNode(text="This is a text node", text_type=TextType.LINK, url=TEST_URL)
        self.assertNotEqual(node_a, node_b)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )
    
    def test_text_node_to_html_node_text(self):
        node = TextNode("This is a text node", TextType.TEXT, "")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node_link(self):
        node = TextNode("Click me!", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_text_node_to_html_node_image(self):
        node = TextNode("Click me!", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.google.com", "alt": "Click me!"})

    def test_text_node_to_html_node_bold(self):
        node = TextNode("Click me!", TextType.BOLD, "")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, None)

    def test_text_node_to_html_node_italic(self):
        node = TextNode("Click me!", TextType.ITALIC, "")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, None)

    def test_text_node_to_html_node_code(self):
        node = TextNode("<script>console.log('Hello, world!');</script>", TextType.CODE, "")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "<script>console.log('Hello, world!');</script>")
        self.assertEqual(html_node.props, None)

if __name__ == "__main__":
    unittest.main()
