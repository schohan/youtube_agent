from pydantic import BaseModel
from typing import Optional
import json
from .topic_ontology import TopicOntology
from app.shared.content.youtube_search import VideoStats


class ResearchedState(BaseModel):
    """
    ResearchedState is a model representing the result of ontology creation for the given topic that has categories and subcategories.

    Attributes:
        topic (TopicOntology): The ontology stored as category > subcategory > children. For example, "Programming" > [ "Python" > ["Django", "Flask"]]
    """          
    input: str
    ontology: TopicOntology = TopicOntology(title="", description="", topics=[])
    videos: list[VideoStats] = []
    is_reviewed: bool = False
    error: str = ""
    success: bool = False


    def __str__(self):
        return f"ResearchedState(input={self.input}, curriculum={self.ontology}, videos={self.videos}, is_reviewed={self.is_reviewed}, error={self.error}, success={self.success})"
    
    def to_dict(self):
        return {
            "input": self.input,
            "ontology": [topic.to_dict() for topic in self.ontology.topics],
            "videos": [video for video in self.videos],
            "is_reviewed": self.is_reviewed,
            "error": self.error,
            "success": self.success
        }
    
    def to_json(self):
        return {
            "input": self.input,
            "ontology": json.dumps([topic.to_dict() for topic in self.ontology.topics], indent=3),
            "videos": json.dumps([video for video in self.videos], indent=3),
            "is_reviewed": self.is_reviewed,
            "error": self.error,
            "success": self.success
        }
    
    def to_json_str(self):
        return json.dumps(self.to_json(), indent=3)