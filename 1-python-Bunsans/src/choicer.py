import random


class Choicer:
    """
    Class with dict_words where key if level and value is list of words with hint
    """

    def __init__(self) -> None:
        self.dict_words = {
            1: [
                ("life", "Duration, existence"),
                ("job", "Task, role, profession"),
                ("work", "Effort, product, manual labor"),
            ],
            2: [
                ("police", "Law enforcement, crime prevention"),
                ("galaxy", "A collection of stars"),
                ("funny", "Amusing, hilarious"),
            ],
            3: [
                ("pneumonia", "Lung infection, bronchi"),
                ("thumbscrew", "Fastener"),
                ("wristwatch", "Timepiece, wrist, watch"),
                ("xylophone", "Musical instrument"),
            ],
        }

    def choice(self, level: str) -> str:
        """
        Choose random word from dict_words with key level, default select level 1
        """
        return random.choice(self.dict_words.setdefault(level, self.dict_words[1]))
