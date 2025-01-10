from pydantic import BaseModel
from typing import Optional
import json
from .topic_ontology import TopicOntology



class ResearchedState(BaseModel):
    """
    ResearchedKeywords is a model representing the result of keyword research grouped into categories and subcategories.

    Attributes:
        keywords (List[MindMapNode]): The keywords stored as category > subcategory > children. For example, "Programming" > [ "Python" > ["Django", "Flask"]]
    """          
    input: str
    curriculum: TopicOntology = TopicOntology(title="", description="", topics=[])
    is_reviewed: bool = False
    error: str = ""
    success: bool = False


    def __str__(self):
        return f"ResearchedState(input={self.input}, curriculum={self.curriculum}, is_reviewed={self.is_reviewed}, error={self.error}, success={self.success})"
    
    def to_dict(self):
        return {
            "input": self.input,
            "curriculum": [keyword.to_dict() for keyword in self.curriculum.topics],
            "is_reviewed": self.is_reviewed,
            "error": self.error,
            "success": self.success
        }
    
    def to_json(self):
        return {
            "input": self.input,
            "keywords": json.dumps([keyword.to_dict() for keyword in self.curriculum.topics], indent=3),
            "is_reviewed": self.is_reviewed,
            "error": self.error,
            "success": self.success
        }
    
    def to_json_str(self):
        return json.dumps(self.to_json(), indent=3)