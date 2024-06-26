from random import choice

from storage import store


def save_words_to_db(words):
    store.append(words)


def get_random_word_from_db():
    return choice(store)
