from pydantic import BaseModel
from typing import Optional
from pydantic import Field
import json

class TopicNode(BaseModel):
    """
    TopicNode is a model representing a node in a mind map.
    """
    title: str = Field(..., description="The title of the topic")
    children: list['TopicNode'] = Field(..., description="The children of the topic")
    

    def to_dict(self):
        return {
            "title": self.title,
            "children": [child.to_dict() for child in self.children] if self.children else []
        }



class TopicOntology(BaseModel):
    """
    TopicOntology is a model representing categories and subcategories in a tree structure.
    """
    title: str = Field(..., description="The title of the ontology")
    description: str = Field(..., description="The description of the ontology")
    topics: list[TopicNode] = Field(default=[], description="The topics of the ontology")


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


    def to_json(self):
        return {
            "title": self.title,
            "description": self.description,
            "topics": json.dumps([topic.to_dict() for topic in self.topics], indent=3)
        }

    def to_json_str(self):
        return json.dumps(self.to_json(), indent=3)



    @staticmethod
    def load_ontology(ontology_json: str | None) -> 'TopicOntology | None':
        """
        Loads topic ontology data from a JSON file and returns a TopicOntology object.
        
        Args:
            ontology_json (str): The JSON string to load
            
        Returns:
            TopicOntology: A TopicOntology object containing the loaded data
        """
        # Read JSON file        
        ontology = None
        if ontology_json:            
            curriculum = ontology_json if isinstance(ontology_json, dict) else json.loads(ontology_json)
            print(f"Curriculum: {curriculum}")
            # Create TopicOntology object
            ontology = TopicOntology(
                title=curriculum.get('title', ''),
                description=curriculum.get('description', ''),
                topics=[TopicNode.model_validate(topic) for topic in curriculum.get('topics', [])]
            )        
            return ontology
        else:
            return None



    def get_keywords(self, input: str) -> dict[str, str]:
        """
        Get the keywords from the ontology as a dictionary. Keywords are only created using titles of leaf objects who has no further children.
        Keys are the concatenation of the titles. Values are the title of the leaf object + the title of the parent objects.
        For example, for input "health" and category "physical health" the keywords are: {"health-physical health-exercise-cardiovascular": "physical health cardiovascular exercise"}
        """
        keywords = {}
        
        def process_node(node: TopicNode, parent_title: str = "", path: list = []):
            current_path = path + [node.title]
            
            if not node.children:  # Leaf node
                # Create key by joining the path with hyphens
                key = input.join("-".join(current_path)).lower()
                # Create value by combining current node title with parent title
                value = f"{parent_title} {node.title}".strip().lower()
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
    ontology_json = json.loads(open('data/test/health-ontology.json', 'r').read())
    print(f"Ontology: {ontology_json}")
    curriculum_data = TopicOntology.load_ontology(ontology_json)
    if curriculum_data:
        print(f"Ontology: {curriculum_data}")
        print(f"Title: {curriculum_data.title}")
        keywords = curriculum_data.get_keywords("health")
        print(f"Keywords: {keywords}")
    else:
        print("No ontology data found")

    assert isinstance(curriculum_data, TopicOntology)
    assert hasattr(curriculum_data, 'title')
    assert hasattr(curriculum_data, 'topics')
    assert curriculum_data.title == "Health"

    
