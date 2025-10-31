class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, 
                 children: list['HTMLNode'] | None = None, props: dict[str, str] | None = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self) -> str:
        raise NotImplementedError
    
    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        
        output_str = ""
        for prop, val in self.props.items():
            output_str += f' {prop}="{val}"'
        return output_str
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, HTMLNode):
            return False
        return (
                self.tag == other.tag
                and self.value == other.value
                and self.children == other.children
                and self.props == other.props
                )
