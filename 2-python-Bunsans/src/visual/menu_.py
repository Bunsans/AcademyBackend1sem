from src.visual.message_phrase import MessageWrongSize
from src.structure_graph import Maze


import os
from typing import Literal

from src.visual.renderer_ import Renderer


class MenuVisualizer:
    def show_menu(self):
        pos_max = self._menu_of_size()
        is_add_surface = self._menu_of_surface()
        is_show_progress = self._menu_of_generation()
        type_of_generation = self._menu_of_type_algo()
        return pos_max, is_add_surface, is_show_progress, type_of_generation

    def _check_coordinate(self, answer: str, max_: int, descr: str) -> bool | str:
        wrong_answer = False
        try:
            answer = int(answer)
            if answer < 0:
                wrong_answer = f"{descr} less than 0"
            if answer > max_:
                wrong_answer = f"{descr} more than {max_}"
        except ValueError:
            wrong_answer = f"{descr} not an int!"
        return wrong_answer

    def _get_from_user(self, descr: str, *args, **kwargs):
        answer = input(descr)
        return answer

    def _check_size(
        self, message_wrong: MessageWrongSize, col_max: str, row_max: str
    ) -> MessageWrongSize:
        try:
            col_max = int(col_max)
            row_max = int(row_max)
            message_wrong.wrong_bound = ""
            if col_max < 5 or row_max < 5:
                message_wrong.wrong_bound = "width or height less than 5"

            if col_max > 49 or row_max > 49:
                if message_wrong.wrong_bound == "":
                    message_wrong.wrong_bound = "width or height more than 49"
                elif message_wrong.wrong_bound == "width or height less than 5":
                    message_wrong.wrong_bound += " or more than 49"

            if col_max % 2 != 1 or row_max % 2 != 1:
                message_wrong.wrong_odd = "width or height not odd"
            else:
                message_wrong.wrong_odd = ""
            message_wrong.wrong_answ = ""
        except ValueError:
            message_wrong.wrong_bound = ""
            message_wrong.wrong_odd = ""
            message_wrong.wrong_answ = "width or height not an int!"
        finally:
            return message_wrong

    def _menu_of_size(self) -> tuple[int, int]:
        """"""
        message_wrong = MessageWrongSize("", "", "")
        os.system("clear")
        print("\n\n")
        while 1:
            if message_wrong.any_wrong():
                message_wrong.print_wrong()
            print("Please choose an odd number starting from 5 to 49")
            col_max = self._get_from_user("Enter width of labirint in format ")
            row_max = self._get_from_user("Enter height of labirint in format ")
            message_wrong: MessageWrongSize = self._check_size(
                message_wrong, col_max, row_max
            )
            os.system("clear")
            if message_wrong.all_not_wrong():
                # to correct visual need shift at 2
                return int(col_max) + 2, int(row_max) + 2

    def _menu_of_surface(self):
        wrong_answer = False
        while 1:
            os.system("clear")
            if wrong_answer:
                print("Wrong answer")
            print("Do you want hard level with different surface?\n")
            answ = self._get_from_user("Press yes/no: ")
            if answ.lower() in ["yes", "y"]:
                return True
            elif answ.lower() in ["no", "n"]:
                return False
            else:
                wrong_answer = True

    def _menu_of_generation(self):
        wrong_answer = False
        while 1:
            os.system("clear")
            if wrong_answer:
                print("Wrong answer")
            print("Do you want see progress of generation of labirint?\n")
            answ = self._get_from_user("Press yes/no: ")
            if answ.lower() in ["yes", "y"]:
                return True
            elif answ.lower() in ["no", "n"]:
                return False
            else:
                wrong_answer = True

    def _menu_of_type_algo(self) -> Literal["prima", "kruskal"]:
        wrong_answer = False
        while 1:
            os.system("clear")
            if wrong_answer:
                print("Wrong answer")
            print("Choose type of generation\n1. Prima\n2. Kruskal\n")
            answ = self._get_from_user("Press number of type: ")
            if answ.lower() in ["1", "prima"]:
                return "prima"
            elif answ.lower() in ["2", "kruskal"]:
                return "kruskal"
            else:
                wrong_answer = True

    def show_choose_begin_final(self, row_max, col_max, renderer: Renderer, maze: Maze):
        wrong_answer = ""
        while 1:
            renderer.print_maze(maze)
            print(wrong_answer)
            print("Select black, pink or brown positions, not white and blue")
            row_begin = self._get_from_user(
                # shift -2 to correct visual
                f"Enter vertical coordinate of begin from {1} to {row_max - 2}: "
            )
            is_answer_wrong = self._check_coordinate(
                row_begin, max_=row_max, descr="Vertical coordinate"
            )
            if is_answer_wrong:
                wrong_answer = is_answer_wrong
                continue

            col_begin = self._get_from_user(
                # shift -2 to correct visual
                f"Enter horizontal coordinate of begin from {1} to {col_max - 2}: "
            )
            is_answer_wrong = self._check_coordinate(
                col_begin, max_=col_max, descr="Horizontal coordinate"
            )
            if is_answer_wrong:
                wrong_answer = is_answer_wrong
                continue

            pos_begin = (int(row_begin), int(col_begin))
            if pos_begin not in maze.nodes:
                wrong_answer = "Sorry it is not in black"
                continue
            row_final = self._get_from_user(
                # shift -2 to correct visual
                f"Enter vertical coordinate of final from {1} to {row_max - 2}: "
            )
            is_answer_wrong = self._check_coordinate(
                row_final, max_=row_max, descr="Vertical coordinate"
            )
            if is_answer_wrong:
                wrong_answer = is_answer_wrong
                continue

            col_final = self._get_from_user(
                # shift -2 to correct visual
                f"Enter horizontal coordinate of final from {1} to {col_max - 2}: "
            )
            is_answer_wrong = self._check_coordinate(
                col_final, max_=col_max, descr="Horizontal coordinate"
            )
            if is_answer_wrong:
                wrong_answer = is_answer_wrong
                continue

            pos_final = (int(row_final), int(col_final))
            if pos_final not in maze.nodes:
                wrong_answer = "Sorry it is not in black"
                continue

            if pos_final == pos_begin:
                wrong_answer = "Sorry begin and final the same, it is not interesting"
                continue

            return pos_begin, pos_final
