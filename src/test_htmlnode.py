import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from functions import text_node_to_html_node

class TestHtmlNode(unittest.TestCase):
    # HTMLNode tests
    def test_eq(self):
        node = HTMLNode("<p>", "Some test text...", None, {"href": "https://www.google.com", "target": "_blank",})
        node2 = HTMLNode("<p>", "Some test text...", None, {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("<p>", "Some test text...", None, {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_neq(self):
        node = HTMLNode("<p>", "Some test text...", {"href": "https://www.google.com", "target": "_blank",})
        self.assertNotEqual(node, "text")

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    # LeafNode tests
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_a_mult_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://example.com/destination-page", "target": "_blank", "rel": "noopener noreferrer"})
        self.assertEqual(node.to_html(), '<a href="https://example.com/destination-page" target="_blank" rel="noopener noreferrer">Click me!</a>')
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    # ParentNode tests
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text")
                ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("p", None)
            node.to_html()

    # text node to html node function tests
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("search", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):
        node = TextNode("image of a flower", TextType.IMAGE, "https://www.kasandbox.org/programming-images/avatars/marcimus-purple.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "https://www.kasandbox.org/programming-images/avatars/marcimus-purple.png", "alt": "image of a flower"})

    def test_invalid_type(self):
        with self.assertRaises(ValueError):
            node = TextNode("Some totally random text..", TextType.TEXT)
            node.text_type = "BOGUS"
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()
