from pydantic import BaseModel
from typing import Optional
from pydantic import Field


class TopicNode(BaseModel):
    """
    TopicNode is a model representing a node in a mind map.
    """
    title: str = Field(..., description="The title of the topic")
    children: Optional[list['TopicNode']] = Field(None, description="The children of the topic")

    def to_dict(self):
        return {
            "title": self.title,
            "children": [child.to_dict() for child in self.children] if self.children else None
        }


class TopicOntology(BaseModel):
    """
    TopicOntology is a model representing categories and subcategories in a tree structure.
    """
    title: str
    description: str
    topics: list[TopicNode]

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "topics": [topic.to_dict() for topic in self.topics]
        }