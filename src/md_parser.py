from textnode import *

def split_nodes_delimiter(old_nodes : TextNode, delimiter, text_type):
    new_nodes = []
    problem_nodes = []
    for node in old_nodes:
        #print(f"starting node: {node}, with delimiter '{delimiter}'")
        split_node = node.text.split(delimiter)
        if len(split_node) % 2:
            #print(f"odd number of parts {split_node}")
            for i in range(len(split_node)):
                if split_node[i] == "":
                    continue
                if i % 2:
                    new_nodes.append(TextNode(split_node[i], text_type))
                    continue
                else:
                    new_nodes.append(TextNode(split_node[i], TextType(node.text_type)))
                    continue
        else:
            #print(f"even number of parts {split_node}")
            #print(f"Incorrect number of subsection on split with '{delimiter}' as delimiter, saving node {node} for later...")
            new_nodes.append(TextNode("TO BE SUBSTITUTED", TextType(node.text_type)))
            problem_nodes.append(node)
    #print(f"\n--------\nfinished with {old_nodes}\n")
    if problem_nodes != [] and len(problem_nodes) % 2 == 0:
        #print(f"\n\nStarting with problem node: {problem_nodes}")
        fixed_nodes = check_merge(problem_nodes, delimiter)
        #print(f"Fixed Nodes: {fixed_nodes}")
        i = 0
        for j in range(len(new_nodes)):
            if i > len(fixed_nodes):
                break
            if i % 2 and new_nodes[j].text_type == TextType.TEXT.value:
                new_nodes[j].text_type = text_type.value
            if i % 2 and new_nodes[j].text_type == TextType.TEXT.value:
                new_nodes[j].text_type = text_type.value
            if new_nodes[j].text == "TO BE SUBSTITUTED":
                #print(f"{new_nodes[j]} {fixed_nodes[i]}")
                new_nodes[j] = TextNode(fixed_nodes[i].text, TextType(fixed_nodes[i].text_type))
                #print(f"{new_nodes[j]} {fixed_nodes[i]}")
                i += 1
        new_nodes = split_nodes_delimiter(new_nodes, delimiter, text_type)
    elif problem_nodes != []:
        raise ValueError(f"Incorrect number of subsection on split with '{delimiter}' as delimiter, and we were not able to fix it")
    return new_nodes

def check_merge(prob, delimiter):
    node1 = prob[0]
    node2 = prob[1]
    node1.text += delimiter
    node2.text = delimiter + node2.text
    if len(prob) > 2:
        return [node1, node2] + check_merge(prob[2:], delimiter)
    return [node1, node2]
    