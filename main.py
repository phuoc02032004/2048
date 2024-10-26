import pygame
import sys
from constants import *
from menu import handle_menu_events, draw_menu
from logicgame import Game, Menu, GUI, ScoreManager

pygame.init()
res = (720, 720)
screen = pygame.display.set_mode(res)
pygame.display.set_caption('2048')

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('2048')

    game_running = False
    game = None
    current_state = "MENU"
    mode_selected = "4 x 4" 
    mode_selected = "6 x 6"   
    show_mode_menu = False

    while True:
        current_state, mode_selected, show_mode_menu = handle_menu_events(screen, current_state, mode_selected, show_mode_menu)

        if current_state == "MENU":
            draw_menu(screen, show_mode_menu, mode_selected)

        elif current_state == "GAME":
            if game is None:
                game = Game(screen, mode_selected)
                for i in range(2):
                    game.generate_tiles(True)
            game.run()

if __name__ == "__main__":
    main()