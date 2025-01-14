from pydantic import BaseModel
from typing import Optional
from pydantic import Field
import json

class TopicNode(BaseModel):
    """
    TopicNode is a model representing a node in a mind map.
    """
    title: str = Field(..., description="The title of the topic")
    children: list['TopicNode'] = Field([], description="The children of the topic")
    

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
    

    def save_to_json(self, file_path: str):
        """Save the ontology to a JSON file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=True, indent=2)
            


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

    def get_keywords(self) -> dict[str, str]:
        """
        Get the keywords from the ontology as a dictionary. Keywords are only created using titles of leaf objects who has no further children.
        Keys are the concatenation of the titles. Values are the title of the leaf object + the title of the parent object.
        For example {"physical health-exercise-cardiovascular": "cardiovascular exercise"}
        """
        keywords = {}
        
        def process_node(node: TopicNode, parent_title: str = "", path: list = []):
            current_path = path + [node.title]
            
            if not node.children:  # Leaf node
                # Create key by joining the path with hyphens
                key = "-".join(current_path).lower()
                # Create value by combining current node title with parent title
                value = f"{node.title} {parent_title}".strip().lower()
                keywords[key] = value
            else:
                # Recursively process children
                for child in node.children:
                    process_node(child, node.title, current_path)
        
        # Process each top-level topic
        for topic in self.topics:
            process_node(topic)
            
        return keywords


if __name__ == "__main__":
    curriculum_data = TopicOntology.load_ontology('data/test/curriculum-ontology.json')
    print(f"Ontology: {curriculum_data}")
    print(f"Title: {curriculum_data.title}")

    assert isinstance(curriculum_data, TopicOntology)
    assert hasattr(curriculum_data, 'title')
    assert hasattr(curriculum_data, 'topics')
    assert curriculum_data.title == "Health"

    keywords = curriculum_data.get_keywords()
    print(f"Keywords: {keywords}")
