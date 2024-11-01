import re

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
    
# def main():
    
#     print(block_to_block_type("ciao"))
    
# main()