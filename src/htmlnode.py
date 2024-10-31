from functools import reduce

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        def prop_to_str(str1, key):
            return str1 + f' {key}="{self.props[key]}"'
        return reduce(prop_to_str, self.props, "")
    
    def __repr__(self):            
        return (
            f"---  HTMLNode  ---\n"
            + f"* Tag: {self.tag}\n"
            + f"* Value: {self.value}\n"
            + f"* Children: {self.children}\n"
            + f"* Props: {self.props}\n"
            + f"--- /HTMLNode  ---"
        )
        
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a Value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent Node must have a tag")
        if self.children is None:
            raise ValueError("Parent Node must have childrem")
        
        html_str = ""
        for child in self.children:
            html_str += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{html_str}</{self.tag}>"
        
        