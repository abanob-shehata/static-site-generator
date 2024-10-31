import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "This is a node value", None, {"href": "https://www.google.com"})
        node2 = HTMLNode("a", "This is a node value", None, {"href": "https://www.google.com"})
        node3 = HTMLNode("b", "This is a node value")
        node4 = HTMLNode()
        self.assertEqual(node.props_to_html(), node2.props_to_html())
        self.assertNotEqual(node3, node2)
        print(node)
        print(node4)
        


if __name__ == "__main__":
    unittest.main()