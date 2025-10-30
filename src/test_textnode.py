import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()
