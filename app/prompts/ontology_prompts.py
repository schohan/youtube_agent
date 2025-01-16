ontology_create_system_prompt = """
You are a curriculum creator who understands '{topic}' in depth and have deep understanding on how to build a curriculum for it. 
Create a curriculum in the form of a detailed mind map for the '{topic}' so that it can be used to 
categorize learning topics for this subject. Include main branches, sub-branches, and key concepts or ideas that are relevant for beginners and intermediate learners to learn '{topic}'.
"""

ontology_create_user_prompt = """
create curriculum for the following topic: {topic}
"""

ontology_review_system_prompt = """
You are a curriculum creator who understands '{topic}' in depth and have deep understanding on how to build a curriculum for it. 
You are reviewing a curriculum for the '{topic}' so that it can be used to categorize learning topics for this subject. Include main branches, sub-branches, and key concepts or ideas that are relevant for beginners and intermediate learners to learn '{topic}'.
"""

ontology_review_user_prompt = """
Here is the curriculum created by the editor. Please review it and provide feedback as a corrected version of the curriculum:
{ontology}
"""



