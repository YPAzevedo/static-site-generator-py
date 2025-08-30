import unittest

from markdown import markdown_to_blocks, split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType


class TestMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://example.com) and [another](https://example.com/another)"
        expected = [("link", "https://example.com"), ("another", "https://example.com/another")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links_single(self):
        text = "This is text with a [boot.dev](https://boot.dev) link"
        expected = [("boot.dev", "https://boot.dev")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links_empty_text(self):
        text = "This is text with a [](https://example.com) link"
        expected = [("", "https://example.com")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links_empty_url(self):
        text = "This is text with a [link]() here"
        expected = [("link", "")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links_no_links(self):
        text = "This is text with no links"
        expected = []
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links_multiple_words(self):
        text = "This is text with a [multiple word link](https://example.com/path) here"
        expected = [("multiple word link", "https://example.com/path")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://example.com/image.jpg) and ![another](https://example.com/another.png)"
        expected = [("image", "https://example.com/image.jpg"), ("another", "https://example.com/another.png")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_images_single(self):
        text = "This is text with an ![alt text](image.jpg) image"
        expected = [("alt text", "image.jpg")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_images_empty_alt(self):
        text = "This is text with an ![](image.jpg) image"
        expected = [("", "image.jpg")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_images_empty_url(self):
        text = "This is text with an ![alt text]() image"
        expected = [("alt text", "")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_images_no_images(self):
        text = "This is text with no images"
        expected = []
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_images_multiple_words(self):
        text = "This is text with an ![multiple word alt text](image.jpg) image"
        expected = [("multiple word alt text", "image.jpg")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_links_and_images_mixed(self):
        text = "This has a [link](https://example.com) and an ![image](image.jpg) together"
        links = extract_markdown_links(text)
        images = extract_markdown_images(text)
        self.assertEqual(links, [("link", "https://example.com")])
        self.assertEqual(images, [("image", "image.jpg")])

    def test_extract_links_excludes_images(self):
        text = "This has a [link](https://example.com) and an ![image](image.jpg) together"
        links = extract_markdown_links(text)
        # Should only return the link, not the image
        self.assertEqual(links, [("link", "https://example.com")])

    def test_extract_images_excludes_links(self):
        text = "This has a [link](https://example.com) and an ![image](image.jpg) together"
        images = extract_markdown_images(text)
        # Should only return the image, not the link
        self.assertEqual(images, [("image", "image.jpg")])
    
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),    
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
