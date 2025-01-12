from pydantic import BaseModel
from typing import Optional
from pydantic import Field
import json

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
    title: str = Field(..., description="The title of the ontology")
    description: str = Field(..., description="The description of the ontology")
    topics: list[TopicNode] = Field(..., description="The topics of the ontology")


    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "topics": [topic.to_dict() for topic in self.topics]
        }
    
    # def load_ontology(file_path: str) -> 'TopicOntology':
    #     """
    #     Create an ontology object using JSON from a file.
    #     """
    #     with open(file_path, 'r') as file:
    #        curriculum_data: TopicOntology = json.load(fp=file)
    #        print(f"Curriculum Data: {curriculum_data}")
    #        return curriculum_data["curriculum"]

    @staticmethod
    def load_ontology(file_path: str) -> 'TopicOntology':
        """
        Loads topic ontology data from a JSON file and returns a TopicOntology object.
        
        Args:
            file_path (str): Path to the JSON file containing the topic ontology data
            
        Returns:
            TopicOntology: A TopicOntology object containing the loaded data
        """
        # Read JSON file
        with open(file_path, 'r') as file:
            curriculum = json.load(file)
        
        # Create TopicOntology object
        ontology = TopicOntology(
            title=curriculum['title'],
            description=curriculum['description'],
            topics=[TopicNode.model_validate(topic) for topic in curriculum['topics']]
        )
        
        return ontology



if __name__ == "__main__":
    curriculum_data = TopicOntology.load_ontology('data/test/curriculum-ontology.json')
    print(f"Ontology: {curriculum_data}")
    print(f"Title: {curriculum_data.title}")

    assert isinstance(curriculum_data, TopicOntology)
    assert hasattr(curriculum_data, 'title')
    assert hasattr(curriculum_data, 'topics')
    assert curriculum_data.title == "Health"
    