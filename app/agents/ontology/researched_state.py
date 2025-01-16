from pydantic import BaseModel
from typing import Optional
import json
from .topic_ontology import TopicOntology
from app.shared.content.youtube_search import VideoStats
from pydantic import Field


class ResearchedState(BaseModel):
    """
    ResearchedState is a model representing the result of ontology creation for the given topic that has categories and subcategories.

    Attributes:
        topic (TopicOntology): The ontology stored as category > subcategory > children. For example, "Programming" > [ "Python" > ["Django", "Flask"]]
    """          
    input: str = Field(default="", description="The input topic for the ontology creation")
    ontology: TopicOntology = Field(default=TopicOntology(title="", description="", topics=[]), description="The ontology created for the given topic")
    ontology_approved: bool = Field(default=False, description="Whether the ontology is approved by the user")
    ontology_review_count: int = Field(default=0, description="The number of times the ontology has been reviewed")
    
    videos: list[VideoStats] = Field(default=[], description="The videos extracted for the ontology")
    error: str = Field(default="", description="The error message if the ontology creation failed")
    success: bool = Field(default=False, description="Whether the ontology creation was successful")


    def __str__(self):
        return f"ResearchedState(input={self.input}, curriculum={self.ontology}, videos={self.videos}, ontology_approved={self.ontology_approved}, error={self.error}, success={self.success})"
    
    def to_dict(self):
        return {
            "input": self.input,
            "ontology": [topic.to_dict() for topic in self.ontology.topics],
            "videos": [video for video in self.videos],
            "ontology_approved": self.ontology_approved,
            "error": self.error,
            "success": self.success
        }
    
    def to_json(self):
        return {
            "input": self.input,
            "ontology": json.dumps([topic.to_dict() for topic in self.ontology.topics], indent=3),
            "videos": json.dumps([video for video in self.videos], indent=3),
            "ontology_approved": self.ontology_approved,
            "error": self.error,
            "success": self.success
        }
    
    def to_json_str(self):
        return json.dumps(self.to_json(), indent=3)