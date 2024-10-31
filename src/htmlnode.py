from functools import reduce

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if isinstance(self.props, dict):
            def prop_to_str(str1, key):
                return str1 + f' {key}="{self.props[key]}"'
            return reduce(prop_to_str, self.props, "")
        raise ValueError("props needs to be a dictionary to call props_to_html")
    
    def __repr__(self):
        child_num = prop_num = 0
        if self.children:
            child_num = len(self.children)
        if self.props:
            prop_num = len(self.props)
            
        return (
            f"---  HTMLNode  ---\n"
            + f"* Tag: {self.tag}\n"
            + f"* Value: {self.value}\n"
            + f"* Children: {child_num}\n"
            + f"* Props: {prop_num}\n"
            + f"--- /HTMLNode  ---"
        )