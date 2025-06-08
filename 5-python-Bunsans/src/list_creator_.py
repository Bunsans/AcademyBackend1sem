from typing import List
import numpy as np


class ListCreator:
    """Class for comparing the speed of creating lists"""

    def comprehension_list(self, length: int) -> List[int]:
        return [el for el in range(length)]

    def loop_list(self, length: int) -> List[int]:
        list_ = []
        for el in range(length):
            list_.append(el)
        return list_

    def numpy_list(self, length: int) -> np.array:
        list_ = np.arange(length)
        return list_
