import random
import sys
import urllib.request
from typing import Tuple, Callable, List

import textdistance


def bullscows(guess: str, riddle: str) -> Tuple[int, int]:
    bulls = textdistance.hamming.similarity(guess, riddle)
    cows = textdistance.bag.similarity(guess, riddle) - bulls
    return bulls, cows


def gameplay(ask: Callable, inform: Callable, words: List[str]) -> int:
    riddle = random.choice(words)
    attempts = 0
    guess = None

    while riddle != guess:
        guess = ask("Введите слово: ", words)
        attempts += 1
        bulls, cows = bullscows(guess, riddle)
        inform("Bulls: {}, Cows: {}", bulls, cows)
    return attempts


def ask(prompt: str, words: List[str] = None) -> str:
    while True:
        try:
            guess = input(prompt)
            break
        except UnicodeDecodeError:
            pass

    if words is not None:
        while guess not in words:
            try:
                guess = input("Слова нет в словаре. " + prompt)
            except UnicodeDecodeError:
                pass
    return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 1 or len(args) > 2:
        raise ValueError("Invalid parameters, use one of the following:\npython3 -m bullscows словарь длина\n"
                         "python3 -m bullscows словарь\n")
    path = args[0]
    if path.startswith("https"):
        words = [line.decode('utf-8').strip() for line in urllib.request.urlopen(path)]
    else:
        with open(path, "r", encoding="utf-8") as f:
            words = [line.strip() for line in f.readlines()]

    word_length = int(args[1]) if len(args) == 2 else 5
    filtered_words = [word for word in words if len(word) == word_length]
    words = filtered_words

    print("Количество попыток: ", gameplay(ask, inform, words))
