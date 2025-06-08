from typing import List


class Concatenator:
    """Class for comparing the speed of concatenating strings in a list"""

    def plus_concatenate(self, list_of_strings: List[str]) -> str:
        result = ""
        for string_ in list_of_strings:
            result += string_
        return result

    def join_concatenate(self, list_of_strings: List[str]) -> str:
        result = "".join(list_of_strings)
        return result
