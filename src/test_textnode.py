import unittest
import re

from textnode import TextNode, TextType
from functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("Test text of the first node", TextType.ITALIC)
        node2 = TextNode("Test text of the second node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("Some random text..", TextType.LINK, "www.testing.com")
        node2 = TextNode("Some random text..", TextType.LINK, "www.testing.com")
        self.assertEqual(node, node2)

    def test_url_neq(self):
        node = TextNode("Random text..", TextType.LINK, "www.testing.com")
        node2 = TextNode("Random text..", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_texttype_ne(self):
        node = TextNode("text...", TextType.ITALIC)
        node2 = TextNode("text...", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    # split_nodes_delimiter() function tests
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("bolded phrase", TextType.BOLD), TextNode(" in the middle", TextType.TEXT)])

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is a text with an _italic_ word in it..", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is a text with an ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" word in it..", TextType.TEXT)])

    def test_missing_delimiter(self):
        node = TextNode("Some random **test text...", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_multiple_delimiters(self):
        node = TextNode("Some **bold** word and other **bold** word..", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("Some ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" word and other ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" word..", TextType.TEXT)])

    def test_multiple_nodes(self):
        node1 = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        node2 = TextNode("code block", TextType.CODE)
        node3 = TextNode("This is text with **more bolded** words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2, node3], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("bolded phrase", TextType.BOLD), TextNode(" in the middle", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode("This is text with ", TextType.TEXT), TextNode("more bolded", TextType.BOLD), TextNode(" words", TextType.TEXT)])

    # Tests for extracting images and links
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
                )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_multiple(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    # Tests for images/links splitting
    def test_split_images_multiple(self):
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

    def test_split_links_multiple(self):
        node = TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.TEXT,
                )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
                [
                    TextNode("This is text with a link ", TextType.TEXT),
                    TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode(
                        "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                        ),
                    ],
                new_nodes,
                )

    def test_split_links_beginning(self):
        node = TextNode(
                "[to boot dev](https://www.boot.dev) a link at the beginning..",
                TextType.TEXT,
                )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
                [
                    TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                    TextNode(" a link at the beginning..", TextType.TEXT),
                    ],
                new_nodes,
                )

    def test_split_images_beginning(self):
        node = TextNode(
                "![image](https://i.imgur.com/zjjcJKZ.png) an image at the beginning..",
                TextType.TEXT,
                )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
                [
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" an image at the beginning..", TextType.TEXT),
                    ],
                new_nodes,
                )

    def test_split_links_end(self):
        node = TextNode(
                "A link at the end.. [to boot dev](https://www.boot.dev)",
                TextType.TEXT,
                )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
                [
		    TextNode("A link at the end.. ", TextType.TEXT),
                    TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                    ],
                new_nodes,
                )

    def test_split_images_end(self):
        node = TextNode(
                "An image at the end.. ![image](https://i.imgur.com/zjjcJKZ.png)",
                TextType.TEXT,
                )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
                [
                    TextNode("An image at the end.. ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    ],
                new_nodes,
                )

    def test_split_links_nolink(self):
        node = TextNode(
                "A text with no link in it..",
                TextType.TEXT,
                )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
                [
		    TextNode("A text with no link in it..", TextType.TEXT),
                    ],
                new_nodes,
                )

    def test_split_images_noimage(self):
        node = TextNode(
                "A text with no image in it..",
                TextType.TEXT,
                )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
                [
                    TextNode("A text with no image in it..", TextType.TEXT),
                    ],
                new_nodes,
                )

if __name__ == "__main__":
    unittest.main()
