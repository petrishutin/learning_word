from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import storage
from ai import get_phrases_from_ai, evaluate_answer_via_ai
from db import save_words_to_db, get_random_word_from_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,  # noqa
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Answer(BaseModel):
    question: str
    answer: str


class Evaluation(BaseModel):
    correct_answer: bool
    justification: str


@app.get('/phrases')
def get_phrases(word: str, ) -> dict:
    phrase = get_phrases_from_ai(word)
    save_words_to_db(phrase)
    return phrase


@app.get('/question')
def get_question():
    word = get_random_word_from_db()
    question = f"Translate to English phrase: {word["phrase"]["phrase_native"]} using word '{word["word_learning"]}'"
    return question


@app.post('/answer')
def get_answer(answer: Answer):
    return evaluate_answer_via_ai(answer.model_dump())


@app.get("/storage")
def get_storage():
    return storage.store
