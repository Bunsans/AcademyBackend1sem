import os
from visual import print_hangman
from choicer import Choicer


class Game:
    """
    Main class of game, contain:
    """

    level: str
    lifes: int
    word: str
    word_len: int
    all_chars: set
    curr_result: str
    max_lifes: int
    predicted_letters: list
    used_letters: list

    def __init__(self, level):
        """
        Call menu of level, in dependence of level choose word and number of lifes
        """
        os.system("clear")
        self.level = level
        os.system("clear")
        dict_of_levels = {1: 10, 2: 8, 3: 6}
        self.lifes = dict_of_levels[self.level]
        self.max_lifes = self.lifes
        self.english_letters = set(i for i in range(97, 123))

    def change_curr_result(self):
        """
        Compare letters in predicted_letters with word and change current result
        """
        for letter in self.word:
            if (
                letter in self.predicted_letters
                or letter.lower() in self.predicted_letters
            ):
                self.curr_result += letter
            else:
                self.curr_result += "_"

    def begin_game(self):
        """
        Begin game session. Every time when user enter letter, check is it english letter and is it in word.
        Call print_stage() with needed phrase.
        """
        # choice word require of level
        self.word, self.hint = Choicer().choice(self.level)
        self.all_chars = set([x.lower() for x in self.word])
        self.word_len = len(self.word)
        self.curr_result = "_" * self.word_len
        self.used_letters = []
        self.predicted_letters = []
        self.print_stage("")
        while 1:
            input_phrase = input("Press enter char: ").lower().rstrip()
            if input_phrase == "hint":
                self.print_stage(self.hint)
                continue
            if len(input_phrase) != 1:
                self.print_stage("Not a letter")
                continue
            asci_char = ord(input_phrase)
            if asci_char not in self.english_letters:
                self.print_stage(
                    "Not an english letter",
                )
                continue
            if input_phrase in self.used_letters:
                self.print_stage(
                    "You have been used this letter",
                )
                continue

            self.used_letters.append(input_phrase)

            self.curr_result = ""

            if input_phrase in self.all_chars:
                self.predicted_letters.append(input_phrase)
                self.change_curr_result()
                self.print_stage("Good!")
            else:
                self.lifes -= 1
                self.change_curr_result()
                self.print_stage("Try again")

            if self.lifes <= 0:
                self.print_stage("Game over")
                break

            if self.curr_result == self.word:
                self.print_stage("You win!")
                break

    def print_stage(self, final_phrase: str):
        """
        Print stage of game depending on letter which was tapped, lifes and word
        """
        os.system("clear")

        print(f"Level: {self.level}")
        print("If you need hint, type 'hint'\n")
        print("lifes: ", f"{self.lifes} / {self.max_lifes}")
        print("Used letters: ", end="")
        if not self.used_letters:
            print("\n")
        else:
            for char in self.used_letters:
                print(char, end=" ")
            print("\n")

        print_hangman(self.lifes)
        print(self.curr_result)
        print(final_phrase)
