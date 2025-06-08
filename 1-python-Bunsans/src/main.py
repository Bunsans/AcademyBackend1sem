import logging

from visual import menu_of_level
from game import Game

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    level = menu_of_level()
    game = Game(level).begin_game()
