import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_value_error(self):
        with self.assertRaises(ValueError) as cm:
            node = HTMLNode(tag="link", value="test", props=None)
            HTMLNode(tag="link", value="test", children=[node], props=None)
        self.assertEqual(str(cm.exception), "HTMLNode can't have value and children")

    def test_set_properties(self):
        node = HTMLNode(tag="link", value="test", props={"href": "test"})

        self.assertIsNotNone(node.tag)
        self.assertIsNotNone(node.value)
        self.assertIsNotNone(node.props)
        self.assertIsNone(node.children)

    def test_props_to_html(self):
        node = HTMLNode(tag="link", value="test", props={"href": "test"})
        html_attr = node.props_to_html()

        self.assertEqual(html_attr, " href=\"test\"")
    
    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )
