import random
from pygame_interface import run_pygame_gui
# bot_called= 1 calls Bot 1, 
# bot_called= 2 calls Bot 2, 
# bot_called= 3 calls Bot 3, 
# bot_called= 4 calls Bot 4, 
# bot_called= 5, is the bonus case where ship environment is also changing. 
run_pygame_gui(40, q=random.random(), bot_called= 5)
