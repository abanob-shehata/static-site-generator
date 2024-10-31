import unittest
from md_parser import split_nodes_delimiter

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_text(self):
        node = TextNode("This *is a text* node", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(nodes, [TextNode("This ", TextType.TEXT), TextNode("is a text", TextType.ITALIC), TextNode(" node", TextType.TEXT)])
    
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
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
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

    def test_nested_delim_code(self):
        node = TextNode("**This is *text* with** a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes2 = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        new_nodes3 = split_nodes_delimiter(new_nodes2, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("**This is *text* with** a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )
        self.assertListEqual(
            [
                TextNode("This is *text* with", TextType.BOLD),
                TextNode(" a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes2,
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.BOLD),
                TextNode("text", TextType.ITALIC),
                TextNode(" with", TextType.BOLD),
                TextNode(" a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes3,
        )

    def test_nested_delim_code_error_prone(self):
        node = TextNode("*This is **text** with a `code block`* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("*This is **text** with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode("* word", TextType.TEXT),
            ],
            new_nodes,
        )
        
        new_nodes2 = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("*This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode("* word", TextType.TEXT),
            ],
            new_nodes2,
        )
        
        new_nodes3 = split_nodes_delimiter(new_nodes2.copy(), "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.ITALIC),
                TextNode("text", TextType.BOLD),
                TextNode(" with a ", TextType.ITALIC),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes3,
        )


if __name__ == "__main__":
    unittest.main()
