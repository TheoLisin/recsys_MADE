import nltk
from nltk.stem import WordNetLemmatizer

from typing import List

lemmatizer = WordNetLemmatizer()
translator = str.maketrans('', '', "!?;(),[].:{}@#$%^&*_")


def tokenize_and_lemmatize(text: str) -> List[str]:
    text = text.translate(translator)
    tokens = [lemmatizer.lemmatize(word.lower()) for sent in nltk.sent_tokenize(
        text) for word in nltk.word_tokenize(sent)]
    return tokens
