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

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Value required.")

        if self.tag is None:
            return self.value

        html_props = self.props_to_html()
        return f"<{self.tag}{html_props}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list['HTMLNode'], props: dict[str,  str] | None = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Missing tag.")

        if self.children is None:
            raise ValueError("Children argument missing.")

        output_html_string = ""
        for child in self.children:
            output_html_string += child.to_html()

        return f"<{self.tag}>{output_html_string}</{self.tag}>"
