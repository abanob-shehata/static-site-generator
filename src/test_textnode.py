import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.TEXT)
        node4 = TextNode("This is a text node", TextType.BOLD, "url")
        self.assertEqual(node, node2)
        self.assertNotEqual(node3, node2)
        self.assertNotEqual(node4, node2)
        


if __name__ == "__main__":
    unittest.main()