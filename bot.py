import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data:dict = json.load(file)
    return data



def save_knowledge_base(file_path : str, data : dict):
    with open(file_path, 'w') as file:
        json.dump( data, file, indent = 2)


def find_best_match(user_question, question): #-> str|None:
    matches: list = get_close_matches(user_question, question, n = 1,cutoff = 0.1)
    return matches[0] if matches else None

def get_answer_for_question(question, knowledge_base: dict): #-> str | None:
    for q in knowledge_base["RESPONSES"]:
        if q["QUESTION"]  == question:
            return q["ANSWERS"]
        


