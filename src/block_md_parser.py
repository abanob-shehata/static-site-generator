import re
from htmlnode import LeafNode, ParentNode
from inline_md_parser import text_to_textnodes
from textnode import text_node_to_html_node

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks if block.strip() != ""]
    return blocks
    
def block_to_block_type(block):
    if re.fullmatch(r"^(#{1,6} .*)", block):
        return "heading"
    elif re.fullmatch(r"^`{3}(.|\s)*`{3}$", block):
        return "code"
    elif re.fullmatch(r"^(> .*)(\n*> .*)*$", block):
        return "quote"
    elif re.fullmatch(r"^([-|*] .*)(\n*[-|*] .*)*$", block):
        return "unordered_list"
    elif re.fullmatch(r"^([\d]+\. .*)(\n*[\d]+\. .*)*$", block):
        return "ordered_list"
    else:
        return "paragraph"
    
def markdown_to_html_node(markdown):
    html_node = ParentNode("div", [])    
    md_blocks = markdown_to_blocks(markdown)
    for md_block in md_blocks:
        block_type = block_to_block_type(md_block)
        match (block_type):
            case ("heading"):
                html_node.children.append(heading_to_html_node(md_block)) 
            case ("code"):
                html_node.children.append(code_to_html_node(md_block))
            case ("quote"):
                html_node.children.append(quote_to_html_node(md_block))
            case ("unordered_list"):
                html_node.children.append(ulist_to_html_node(md_block))
            case ("ordered_list"):
                html_node.children.append(olist_to_html_node(md_block))
            case ("paragraph"):
                html_node.children.append(par_to_html_node(md_block))
            case _:
                raise ValueError("Incorrect Block Type")
    return html_node
    
def heading_to_html_node(block):
    text, count = remove_until_with_count(block, " ", 0)
    return LeafNode(f"h{count}", text)
    
def code_to_html_node(block):
    return ParentNode("pre", [
        LeafNode("code", block[3:-3].strip())
    ])

def quote_to_html_node(block):
    quote_node = ParentNode("blockquote", [])
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(remove_until(line, " "))
    text_nodes = text_to_textnodes(" ".join(new_lines))
    for node in text_nodes:
        quote_node.children.append(text_node_to_html_node(node))
    return quote_node

def ulist_to_html_node(block):
    ulist_node = ParentNode("ul", [])
    lines = block.split("\n")
    for line in lines:
        ulist_node.children.append(ParentNode("li", []))
        text_nodes = text_to_textnodes(remove_until(line, " "))
        for node in text_nodes:
            ulist_node.children[-1].children.append(text_node_to_html_node(node))
    return ulist_node

def olist_to_html_node(block):
    olist_node = ParentNode("ol", [])
    lines = block.split("\n")
    for line in lines:
        olist_node.children.append(ParentNode("li", []))
        text_nodes = text_to_textnodes(remove_until(line, " "))
        for node in text_nodes:
            olist_node.children[-1].children.append(text_node_to_html_node(node))
    return olist_node

def par_to_html_node(block):
    text_nodes = text_to_textnodes(" ".join(block.split("\n")))
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return ParentNode("p", html_nodes)

def remove_until_with_count(text, char, count):
        if text[0] == char:
            return text[1:], count
        count += 1
        return remove_until_with_count(text[1:], char, count)
    
def remove_until(text, char):
        if text[0] == char:
            return text[1:]
        return remove_until(text[1:], char)

# def main():
    
#     print(markdown_to_html_node("""
# - This is a list
# - with `items`
# - and *more* items
# """))
    
# main()