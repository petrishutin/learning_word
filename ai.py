import json

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

model = ChatOpenAI(model="gpt-4")


def get_phrases_from_ai(word: str) -> dict:
    system_message = """ 
    User inputs word (word_learning)
    Translate word to russian (word_native)
    Come up with a phrase containing the user's word (phrase_learning) and translate it into Russian (phrase_native)
    Answer in JSON format ONLY like: 
    {
        "word_native": "толераноность", "word_learning": "tolerance",
        "phrase": {"phrase_native": "нулевая терпимость", "phrase_learning": "zero tolerance"}
    }
    """

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=word),
    ]

    result = model.invoke(messages)
    result_json = json.loads(result.content)
    return result_json


def evaluate_answer_via_ai(answer: dict) -> dict:
    system_message = f""" 
    The task for user was: {answer["question"]}
    Evaluate user's answer 
    and say if answer is correct (true or false) and give it the correct. 
    Answer in JSON format ONLY like: 
    {{"correct": <true | false>,
      "justification": <your correct answer for this question and justification
    }}
    """

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=answer["answer"]),
    ]

    result = model.invoke(messages)
    result_json = json.loads(result.content)
    return result_json
