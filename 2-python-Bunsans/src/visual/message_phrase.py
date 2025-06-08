from dataclasses import dataclass
from typing import Literal


@dataclass
class MessageWrongSize:
    wrong_answ: Literal["", "width or height not an int!"]
    wrong_bound: Literal[
        "",
        "width or height less than 5",
        "width or height more than 49",
        "width or height less than 5 or more than 49",
    ]
    wrong_odd: Literal["", "width or height not odd"]

    # def __eq__(self, value: object) -> bool:
    #     return (
    #         self.wrong_answ == value.wrong_answ
    #         and self.wrong_bound == value.wrong_bound
    #         and self.wrong_odd == value.wrong_odd
    #     )

    def any_wrong(self):
        return (
            (self.wrong_answ != "")
            or (self.wrong_bound != "")
            or (self.wrong_odd != "")
        )

    def all_not_wrong(self):
        return (
            (self.wrong_answ == "")
            and (self.wrong_bound == "")
            and (self.wrong_odd == "")
        )

    def print_wrong(self):
        print(self.wrong_answ + "\n" + self.wrong_bound + "\n" + self.wrong_odd)
