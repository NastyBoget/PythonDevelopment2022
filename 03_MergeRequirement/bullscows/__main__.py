from typing import Tuple, Callable, List
import textdistance
import random
import sys


def bullscows(guess: str, riddle: str) -> Tuple[int, int]:
    bulls = textdistance.hamming.similarity(guess, riddle)
    cows = textdistance.bag.similarity(guess, riddle) - bulls
    return bulls, cows


def gameplay(ask: Callable, inform: Callable, words: List[str]) -> int:
    riddle = random.choice(words)
    attempts = 0
    guess = None

    while riddle != guess:
        guess = ask("Введите слово: ")
        attempts += 1
        bulls, cows = bullscows(guess, riddle)
        inform("Bulls: {}, Cows: {}", bulls, cows)
    return attempts


def ask(prompt: str, words: List[str] = None) -> str:
    guess = input(prompt)
    if words is not None:
        while guess not in words:
            guess = input("Слова нет в словаре. " + prompt)
    return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


if __name__ == "__main__":
    args = sys.argv[1:]
