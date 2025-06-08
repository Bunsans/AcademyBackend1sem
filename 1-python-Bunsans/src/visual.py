import os


def print_hangman(lifes: int) -> None:
    """"""
    print(" " * 4 + "_" * 6)
    for i in range(8):
        print(" " * 4 + "|" + " " * 3, end="")

        if lifes <= 9 and i == 0:
            print("  |", end="")

        if lifes <= 8 and i == 1:
            print("  |", end="")

        if lifes <= 7 and i == 2:
            print("  |", end="")

        if lifes <= 6 and i == 3:
            print("  |", end="")

        if lifes <= 5 and i == 4:
            print("  O", end="")
        if i == 5:
            if lifes <= 4:
                print("/", end="")
            if lifes <= 3:
                print("| |", end="")
            if lifes <= 2:
                print("\\", end="")
        if i == 6:
            if lifes <= 1:
                print(" /", end="")
            if lifes <= 0:
                print(" \\", end="")
        print("")
    print("-" * 15)


def menu_of_level() -> int:
    """"""
    level = 1
    wrong_answer = False
    while 1:
        os.system("clear")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        print("4. Exit\n")

        if wrong_answer:
            print("Wrong answer")

        level = input("Enter number from 1 to 4 to choose level: ")
        if level == "4":
            os.system("clear")
            exit()
        if level in ["1", "2", "3", "4"]:
            return int(level)
        else:
            wrong_answer = True
