import pygame
import sys
from constants import *
import numpy as np
import random

pygame.init()

# Khởi tạo màn hình
res = (720, 720)
screen = pygame.display.set_mode(res)
pygame.display.set_caption('2048')

width = screen.get_width()
height = screen.get_height()

# Khởi tạo font chữ
smallfont = pygame.font.SysFont('Corbel', 35)
# Tính toán vị trí của text cho các button
text_start = smallfont.render('Start', True, color)
text_start_rect = text_start.get_rect(center=(180 + 130 // 2, 180 + 55 // 2))
text_mode = smallfont.render('Mode', True, color)
text_mode_rect = text_mode.get_rect(center=(180 + 130 // 2, 180 + 55 // 2 + 70))
text_setting = smallfont.render('Setting', True, color)
text_setting_rect = text_setting.get_rect(center=(180 + 130 // 2, 250 + 55 // 2 + 70))  # Tăng vị trí cho button Setting
text_exit = smallfont.render('Exit', True, color)
text_exit_rect = text_exit.get_rect(center=(180 + 130 // 2, 320 + 55 // 2 + 70))  # Tăng vị trí cho button Exit

text_normal = smallfont.render('Normal', True, color)
text_normal_rect = text_normal.get_rect(center=(180 + 130 // 2, 180 + 55 // 2 + 140))
text_challenge = smallfont.render('Challenge', True, color)
text_challenge_rect = text_challenge.get_rect(center=(180 + 130 // 2, 180 + 55 // 2 + 210))

# Biến trạng thái trò chơi
game_running = False
game = None
current_state = "MENU"
mode_selected = "NORMAL"  
show_mode_menu = False

class ScoreManager:
    def __init__(self):
        self.score = 0
        self.best = 0

    def check_highscore(self):
        if self.score >= self.best:
            self.best = self.score

    def reset_score(self):
        self.score = 0

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.transparent_screen = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
        self.transparent_screen.set_alpha(TRANSPARENT_ALPHA)
        self.transparent_screen.fill(WHITE)
        self.go_font = pygame.font.SysFont('verdana', 30, True)
        self.go_lbl = self.go_font.render('Game over!', 1, GAMEOVER_LBL_COLOR)
        self.go_pos = (XSHIFT + BOARD_WIDTH // 2 - self.go_lbl.get_rect().width // 2, YSHIFT3 + BOARD_HEIGHT // 2 - self.go_lbl.get_rect().height // 2 - 35)
        self.tryagain_btn = pygame.image.load('./images/tryagain_btn.png')
        self.tryagain_btn = pygame.transform.scale(self.tryagain_btn, (115, 40))
        self.tryagain_btn_pos = (XSHIFT + BOARD_WIDTH // 2 - self.tryagain_btn.get_width() // 2, YSHIFT3 + BOARD_HEIGHT // 2 - self.tryagain_btn.get_height() // 2 + 35)
        self.tryagain_btn_rect = self.tryagain_btn.get_rect(topleft=self.tryagain_btn_pos)
        self.active = False

    def show(self):
        if self.active:
            self.screen.blit(self.transparent_screen, (XSHIFT, YSHIFT3))
            self.screen.blit(self.go_lbl, self.go_pos)
            self.screen.blit(self.tryagain_btn, self.tryagain_btn_pos)

    def hide(self, bg):
        self.active = False
        pygame.draw.rect(self.screen, BOARD_COLOR, bg)

class GUI:
    def __init__(self, screen):
        self.screen = screen
        self.logo = pygame.image.load('./images/logo.png')
        self.logo = pygame.transform.scale(self.logo, (self.logo.get_width() // 2, self.logo.get_height() // 2))
        self.logo_pos = (XSHIFT, YSHIFT)
        self.score_rect = pygame.image.load('./images/score_rect.png')
        self.score_rect = pygame.transform.scale(self.score_rect, (90, 42))
        self.score_rect_pos = (XSHIFT2, YSHIFT)
        self.best_rect = pygame.image.load('./images/best_rect.png')
        self.best_rect = pygame.transform.scale(self.best_rect, (90, 42))
        self.best_rect_pos = (XSHIFT2 + self.score_rect.get_width() + 2, YSHIFT)
        self.score_font = pygame.font.SysFont('verdana', 15, bold=True)
        self.message = pygame.image.load('./images/message.png')
        self.message = pygame.transform.scale(self.message, (self.message.get_width() // 2, self.message.get_height() // 2))
        self.message_pos = (XSHIFT, YSHIFT2)
        self.newgame_btn = pygame.image.load('./images/newgame_btn.png')
        self.newgame_btn = pygame.transform.scale(self.newgame_btn, (115, 40))
        self.newgame_btn_pos = (XSHIFT3, YSHIFT2)
        self.newgame_btn_rect = self.newgame_btn.get_rect(topleft=self.newgame_btn_pos)
        self.board_rect = (XSHIFT, YSHIFT3, BOARD_WIDTH, BOARD_HEIGHT)
        self.menu = Menu(screen)

    def show_start(self):
        self.screen.blit(self.newgame_btn, self.newgame_btn_pos)

    def update_scores(self, score_value, best_value):
        self.screen.blit(self.score_rect, self.score_rect_pos)
        self.score_lbl = self.score_font.render(str(score_value), 0, WHITE)
        self.score_pos = (XSHIFT2 + self.score_rect.get_width() // 2 - self.score_lbl.get_rect().width // 2, YSHIFT + self.score_rect.get_height() // 2 - self.score_lbl.get_rect().height // 2 + 8)
        self.screen.blit(self.score_lbl, self.score_pos)
        self.screen.blit(self.best_rect, self.best_rect_pos)
        self.best_lbl = self.score_font.render(str(best_value), 0, WHITE)
        self.best_pos = (290 + self.best_rect.get_width() // 2 - self.best_lbl.get_rect().width // 2, YSHIFT + self.best_rect.get_height() // 2 - self.best_lbl.get_rect().height // 2 + 8)
        self.screen.blit(self.best_lbl, self.best_pos)

    def action_listener(self, event):
        if self.menu.active:
            if self.menu.tryagain_btn_rect.collidepoint(event.pos):
                self.menu.hide(self.board_rect)
                return True
        elif self.newgame_btn_rect.collidepoint(event.pos):
            return True
        return False

class Game:
    def __init__(self, screen, mode):
        self.screen = screen
        self.tiles = np.zeros((ROWS, COLS))
        self.gui = GUI(screen)
        self.score_manager = ScoreManager()
        self.lbl_font = pygame.font.SysFont('verdana', 30, bold=True)
        self.generate = False
        self.playing = True
        self.mode = mode

    def draw_board(self):
        pygame.draw.rect(self.screen, BOARD_COLOR, self.gui.board_rect)

        rShift, cShift = GAP, GAP
        for row in range(ROWS):
            for col in range(COLS):
                tile_num = int(self.tiles[row][col])
                tile_color = TILES_COLORS[tile_num]
                pygame.draw.rect(self.screen, tile_color, (XSHIFT + cShift + col * TILE_SIZE, YSHIFT3 + rShift + row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                tile_lbl_color = LBLS_COLORS[tile_num]
                lbl = self.lbl_font.render(str(tile_num), 0, tile_lbl_color)
                lbl_pos = (XSHIFT + cShift + col * TILE_SIZE + TILE_SIZE // 2 - lbl.get_rect().width // 2, YSHIFT3 + rShift + row * TILE_SIZE + TILE_SIZE // 2 - lbl.get_rect().height // 2)
                self.screen.blit(lbl, lbl_pos)
                cShift += GAP
            rShift += GAP
            cShift = GAP

        self.screen.blit(self.gui.logo, self.gui.logo_pos)
        self.screen.blit(self.gui.message, self.gui.message_pos)

    def generate_tiles(self, first=False):
        empty_tiles = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.tiles[row][col] == 0:
                    empty_tiles.append((row, col))
        idx = random.randrange(0, len(empty_tiles))
        row, col = empty_tiles[idx]
        rnd = random.randint(1, 10)
        tile_value = 2
        # Tăng xác suất xuất hiện số 4 trong chế độ Challenge
        if self.mode == "CHALLENGE" and not first and rnd > 5:
            tile_value = 4
        elif not first and rnd > 7:
            tile_value = 4
        self.tiles[row][col] = tile_value

    def __move_and_merge(self, direction, row, col):
        dx, dy = 0, 0
        if direction == 'UP':
            dy = -1
        elif direction == 'DOWN':
            dy = 1
        elif direction == 'RIGHT':
            dx = 1
        elif direction == 'LEFT':
            dx = -1
        try:
            if self.tiles[row + dy][col + dx] == 0:
                value = self.tiles[row][col]
                self.tiles[row][col] = 0
                self.tiles[row + dy][col + dx] = value
                self.generate = True
                self.__move_and_merge(direction, row + dy, col + dx)
            elif self.tiles[row][col] == self.tiles[row + dy][col + dx]:
                self.tiles[row][col] = 0
                self.tiles[row + dy][col + dx] *= 2
                self.score_manager.score += int(self.tiles[row + dy][col + dx])
                self.generate = True
        except IndexError:
            return

    def slide_tiles(self, direction):
        if direction == 'UP':
            for row in range(1, ROWS):
                for col in range(COLS):
                    if self.tiles[row][col] != 0:
                        self.__move_and_merge(direction, row, col)
        if direction == 'DOWN':
            for row in range(ROWS - 2, -1, -1):
                for col in range(COLS):
                    if self.tiles[row][col] != 0:
                        self.__move_and_merge(direction, row, col)
        if direction == 'RIGHT':
            for row in range(ROWS):
                for col in range(COLS - 2, -1, -1):
                    if self.tiles[row][col] != 0:
                        self.__move_and_merge(direction, row, col)
        if direction == 'LEFT':
            for row in range(ROWS):
                for col in range(1, COLS):
                    if self.tiles[row][col] != 0:
                        self.__move_and_merge(direction, row, col)

    def __full_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.tiles[row][col] == 0:
                    return False
        return True

    def __no_more_moves(self):
        for row in range(1, ROWS):
            for col in range(COLS):
                if self.tiles[row][col] == self.tiles[row - 1][col]:
                    return False
        for row in range(ROWS - 2, -1, -1):
            for col in range(COLS):
                if self.tiles[row][col] == self.tiles[row + 1][col]:
                    return False
        for row in range(ROWS):
            for col in range(COLS - 2, -1, -1):
                if self.tiles[row][col] == self.tiles[row][col + 1]:
                    return False
        for row in range(ROWS):
            for col in range(1, COLS):
                if self.tiles[row][col] == self.tiles[row][col - 1]:
                    return False
        return True

    def is_game_over(self):
        if self.__full_board():
            return self.__no_more_moves()
        return False

    def new(self):
        self.tiles = np.zeros((ROWS, COLS))
        self.score_manager.reset_score()
        self.generate_tiles()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('2048')

    game_running = False
    game = None
    current_state = "MENU"
    mode_selected = "NORMAL"  
    show_mode_menu = False

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                button_width = 130
                button_x = 180
                button_y = 180
                # Button Start
                if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + 50:
                    if current_state == "MENU":
                        current_state = "GAME"
                        if game is None:
                            game = Game(screen, mode_selected)
                            for i in range(2):
                                game.generate_tiles(True)
                        pygame.display.update()
                # Button Mode
                button_y = 180 + 70  # Vị trí button Mode
                if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + 50:
                    show_mode_menu = not show_mode_menu
                # Button Setting
                button_y = 250 + 70  # Tăng vị trí cho button Setting
                if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + 50:
                    # Điền vào chức năng cho Setting
                    print("Setting button clicked")
                    # ...
                # Button Exit
                button_y = 320 + 70  # Tăng vị trí cho button Exit
                if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + 50:
                    pygame.quit()
                    sys.exit()
                # Button Normal
                button_y = 180 + 55 + 140
                if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + 50 and show_mode_menu:
                    mode_selected = "NORMAL"
                    show_mode_menu = False
                # Button Challenge
                button_y = 180 + 55 + 210
                if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + 50 and show_mode_menu:
                    mode_selected = "CHALLENGE"
                    show_mode_menu = False

        if current_state == "MENU":
            screen.fill(SCREEN_COLOR)
            mouse = pygame.mouse.get_pos()
            # Vẽ button Start
            button_width = 130
            button_x = 180
            button_y = 180
            if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + 50:
                pygame.draw.rect(screen, color_light, [button_x, button_y, button_width, 55])
            else:
                pygame.draw.rect(screen, color_dark, [button_x, button_y, button_width, 55])
            screen.blit(text_start, text_start_rect) 

            # Vẽ button Mode
            button_y = 180 + 70  
            if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + 50:
                pygame.draw.rect(screen, color_light, [button_x, button_y, button_width, 55])
            else:
                pygame.draw.rect(screen, color_dark, [button_x, button_y, button_width, 55])
            screen.blit(text_mode, text_mode_rect) 

            # Vẽ button Setting
            button_y = 250 + 70  # Tăng vị trí cho button Setting
            if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + 50:
                pygame.draw.rect(screen, color_light, [button_x, button_y, button_width, 55])
            else:
                pygame.draw.rect(screen, color_dark, [button_x, button_y, button_width, 55])
            screen.blit(text_setting, text_setting_rect) 

            # Vẽ button Exit
            button_y = 320 + 70  # Tăng vị trí cho button Exit
            if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + 50:
                pygame.draw.rect(screen, color_light, [button_x, button_y, button_width, 55])
            else:
                pygame.draw.rect(screen, color_dark, [button_x, button_y, button_width, 55])
            screen.blit(text_exit, text_exit_rect) 

            # Hiển thị menu Mode nếu cần
            if show_mode_menu:
                # Vẽ button Normal
                button_y = 180 + 140 
                if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + 50:
                    pygame.draw.rect(screen, color_light, [button_x, button_y, button_width, 55])
                else:
                    pygame.draw.rect(screen, color_dark, [button_x, button_y, button_width, 55])
                screen.blit(text_normal, text_normal_rect)  
                # Vẽ button Challenge
                button_y = 180 + 210
                if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + 50:
                    pygame.draw.rect(screen, color_light, [button_x, button_y, button_width, 55])
                else:
                    pygame.draw.rect(screen, color_dark, [button_x, button_y, button_width, 55])
                screen.blit(text_challenge, text_challenge_rect)  
                
            if game is not None:
                game.gui.show_start()
            pygame.display.update()
        elif current_state == "GAME":
            if game is not None:
                screen.fill(SCREEN_COLOR)

                game.draw_board()
                game.gui.menu.show()
                game.gui.update_scores(game.score_manager.score, game.score_manager.best)
                if game.is_game_over():
                    game.gui.menu.active = True
                game.score_manager.check_highscore()

                game.gui.show_start()

                pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game.slide_tiles('UP')
                    if event.key == pygame.K_DOWN:
                        game.slide_tiles('DOWN')
                    if event.key == pygame.K_RIGHT:
                        game.slide_tiles('RIGHT')
                    if event.key == pygame.K_LEFT:
                        game.slide_tiles('LEFT')
                    if game.generate:
                        game.generate_tiles()
                        game.generate = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if game.gui.action_listener(event):
                            game.new()

if __name__ == "__main__":
    main()