import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_value_error(self):
        node = LeafNode(tag="p", value=None)
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "All LeafNodes must have value")

    def test_set_properties(self):
        node = LeafNode(tag="link", value="test", props={"href": "test"})

        self.assertIsNotNone(node.tag)
        self.assertIsNotNone(node.value)
        self.assertIsNotNone(node.props)
        self.assertIsNone(node.children)

    def test_link(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_p(self):
        node = LeafNode("p", "This is a paragraph of text.")

        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_repr(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(
            repr(node),
            "LeafNode(p, This is a paragraph of text., None)",
        )
