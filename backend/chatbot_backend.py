import json
from difflib import get_close_matches


def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def find_best_match(user_question: str, questions: list[str], cutoff: float = 0.6) -> str | None:
    match = get_close_matches(user_question, questions, n=1, cutoff=cutoff)
    return match[0] if match else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    return next((q["answer"] for q in knowledge_base["question"] if q["question"] == question), None)


def search_response( user_input: str, knowledge_base: dict ):
    user_input = user_input.lower()


    if user_input.lower() == 'quit':
        return knowledge_base['farewell_response'], True
  

    best_match: str | None = find_best_match( user_input, [q["question"] for q in knowledge_base["question"]] )
    if best_match:
        answer: str = get_answer_for_question( best_match, knowledge_base )
        return answer, False

    return knowledge_base['response_not_found'], False
