import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html_shouldReturnWellFormatedtring(self):
        htmlNode = HTMLNode(props={"href":"https://www.google.com"})
        self.assertEqual(htmlNode.props_to_html(), ' href="https://www.google.com"')
    def test_props_to_html_IfNotParametersShouldReturn(self):
        htmlNode = HTMLNode()
        self.assertEqual(htmlNode.props_to_html(), "")
    def test_props_to_html_Needs_Leading_And_Trailing_Whitespace(self):
        htmlNode = HTMLNode(props={"href":"https://www.google.com"})
        stringToAssert = htmlNode.props_to_html()
        if stringToAssert is not None:
            self.assertEqual(stringToAssert[0], " ")
            self.assertNotEqual(stringToAssert[-1], " ")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_div(self):
        node = LeafNode("div", "Hello, I am a leaf node")
        self.assertEqual(node.to_html(), "<div>Hello, I am a leaf node</div>")
    def test_leaf_to_html_without_value(self):
        with self.assertRaises(ValueError):
            LeafNode("div", None).to_html()

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
    def test_to_html_many_children(self):
        node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                    ],
                )
        self.assertEqual(
                node.to_html(),
                "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
                )

    def test_headings(self):
        node = ParentNode(
                "h2",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                    ],
                )
        self.assertEqual(
                node.to_html(),
                "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
                )


