import pygame
import sys
import numpy as np
import random
from constants import *

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
        self.go_pos = (XSHIFT + BOARD_WIDTH // 2 - self.go_lbl.get_rect().width // 2, 
                       YSHIFT3 + BOARD_HEIGHT // 2 - self.go_lbl.get_rect().height // 2 - 35)
        self.tryagain_btn = pygame.image.load('./images/tryagain_btn.png')
        self.tryagain_btn = pygame.transform.scale(self.tryagain_btn, (115, 40))
        self.tryagain_btn_pos = (XSHIFT + BOARD_WIDTH // 2 - self.tryagain_btn.get_width() // 2,
                                 YSHIFT3 + BOARD_HEIGHT // 2 - self.tryagain_btn.get_height() // 2 + 35)
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

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.transparent_screen = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
        self.transparent_screen.set_alpha(TRANSPARENT_ALPHA)
        self.transparent_screen.fill(WHITE)
        self.pause_font = pygame.font.SysFont('verdana', 30, True)
        self.pause_lbl = self.pause_font.render('Paused', 1, GAMEOVER_LBL_COLOR)
        self.pause_pos = (XSHIFT + BOARD_WIDTH // 2 - self.pause_lbl.get_rect().width // 2, 
                       YSHIFT3 + BOARD_HEIGHT // 2 - self.pause_lbl.get_rect().height // 2 - 35)
        
        self.resume_btn = pygame.image.load('./images/icon_continue.png')
        self.resume_btn = pygame.transform.scale(self.resume_btn, (150, 50))
        self.resume_btn_pos = (XSHIFT + BOARD_WIDTH // 2 - self.resume_btn.get_width() // 2,
                               YSHIFT3 + BOARD_HEIGHT // 2 - self.resume_btn.get_height() // 2 + 10)
        self.resume_btn_rect = self.resume_btn.get_rect(topleft=self.resume_btn_pos)


        self.back_btn = pygame.image.load('./images/icon_back.png')
        self.back_btn = pygame.transform.scale(self.back_btn, (115, 40))
        self.back_btn_pos = (XSHIFT + BOARD_WIDTH // 2 - self.back_btn.get_width() // 2,
                                 YSHIFT3 + BOARD_HEIGHT // 2 - self.back_btn.get_height() // 2 + 80)
        self.back_btn_rect = self.back_btn.get_rect(topleft=self.back_btn_pos)
        self.active = False

    def show(self):
        if self.active:
            self.screen.blit(self.transparent_screen, (XSHIFT, YSHIFT3))
            self.screen.blit(self.pause_lbl, self.pause_pos)
            self.screen.blit(self.resume_btn, self.resume_btn_pos)
            self.screen.blit(self.back_btn, self.back_btn_pos)

    def hide(self, bg):
        self.active = False
        pygame.draw.rect(self.screen, BOARD_COLOR, bg)

class GUI:
    def __init__(self, screen, mode):
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
        
        if mode == "4 x 4":
            self.board_rect = (XSHIFT, YSHIFT3, BOARD_WIDTH, BOARD_HEIGHT)
        elif mode == "6 x 6":
            self.board_rect = (XSHIFT, YSHIFT3, BOARD_WIDTH + 136, BOARD_HEIGHT + 136)
        
        self.menu = Menu(screen)
        self.pause_menu = PauseMenu(screen)
        self.pause_btn = pygame.image.load('./images/btn_pause.png')
        self.pause_btn = pygame.transform.scale(self.pause_btn, (40, 40))
        self.pause_btn_pos = (XSHIFT2 + self.score_rect.get_width() + 2 + self.best_rect.get_width() + 2, YSHIFT)
        self.pause_btn_rect = self.pause_btn.get_rect(topleft=self.pause_btn_pos)

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
        self.screen.blit(self.pause_btn, self.pause_btn_pos)

    def action_listener(self, event):
        if self.pause_menu.active:
            if self.pause_menu.back_btn_rect.collidepoint(event.pos):
                self.pause_menu.hide(self.board_rect)
                return 'MENU'
            elif self.pause_menu.resume_btn_rect.collidepoint(event.pos):
                self.pause_menu.hide(self.board_rect)
        elif self.menu.active:
            if self.menu.tryagain_btn_rect.collidepoint(event.pos):
                self.menu.hide(self.board_rect)
                return True
        elif self.newgame_btn_rect.collidepoint(event.pos):
            return True
        elif self.pause_btn_rect.collidepoint(event.pos):
            self.pause_menu.active = not self.pause_menu.active
        return False

class Game:
    def __init__(self, screen, mode):
        self.screen = screen
        self.mode = mode
        if self.mode == "4 x 4":
            self.tiles = np.zeros((4, 4))
        elif self.mode == "6 x 6":
            self.tiles = np.zeros((6, 6))
        
        self.gui = GUI(screen, self.mode)
        self.score_manager = ScoreManager()
        self.lbl_font = pygame.font.SysFont('verdana', 30, bold=True)
        self.generate = False
        self.playing = True

    def draw_board(self):
        pygame.draw.rect(self.screen, BOARD_COLOR, self.gui.board_rect)

        rShift, cShift = GAP, GAP
        for row in range(self.tiles.shape[0]):
            for col in range(self.tiles.shape[1]):
                tile_num = int(self.tiles[row][col])
                tile_color = TILES_COLORS[tile_num]
                pygame.draw.rect(self.screen, tile_color, (XSHIFT + cShift + col * TILE_SIZE, 
                                                           YSHIFT3 + rShift + row * TILE_SIZE, 
                                                           TILE_SIZE, TILE_SIZE))
                tile_lbl_color = LBLS_COLORS[tile_num]
                lbl = self.lbl_font.render(str(tile_num), 0, tile_lbl_color)
                lbl_pos = (XSHIFT + cShift + col * TILE_SIZE + TILE_SIZE // 2 - lbl.get_rect().width // 2, 
                           YSHIFT3 + rShift + row * TILE_SIZE + TILE_SIZE // 2 - lbl.get_rect().height // 2)
                self.screen.blit(lbl, lbl_pos)
                cShift += GAP
            rShift += GAP
            cShift = GAP

        self.screen.blit(self.gui.logo, self.gui.logo_pos)
        self.screen.blit(self.gui.message, self.gui.message_pos)

    def generate_tiles(self, first=False):
        empty_tiles = []
        for row in range(self.tiles.shape[0]):
            for col in range(self.tiles.shape[1]):
                if self.tiles[row][col] == 0:
                    empty_tiles.append((row, col))
        idx = random.randrange(0, len(empty_tiles))
        row, col = empty_tiles[idx]
        rnd = random.randint(1, 10)
        tile_value = 2
        if self.mode == "4 x 4" and not first and rnd > 8:
            tile_value = 4
        elif self.mode == "6 x 6" and not first and rnd > 4:
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
            for row in range(1, self.tiles.shape[0]):
                for col in range(self.tiles.shape[1]):
                    if self.tiles[row][col] != 0:
                        self.__move_and_merge(direction, row, col)
        if direction == 'DOWN':
            for row in range(self.tiles.shape[0] - 2, -1, -1):
                for col in range(self.tiles.shape[1]):
                    if self.tiles[row][col] != 0:
                        self.__move_and_merge(direction, row, col)
        if direction == 'RIGHT':
            for row in range(self.tiles.shape[0]):
                for col in range(self.tiles.shape[1] - 2, -1, -1):
                    if self.tiles[row][col] != 0:
                        self.__move_and_merge(direction, row, col)
        if direction == 'LEFT':
            for row in range(self.tiles.shape[0]):
                for col in range(1, self.tiles.shape[1]):
                    if self.tiles[row][col] != 0:
                        self.__move_and_merge(direction, row, col)

    def __full_board(self):
        for row in range(self.tiles.shape[0]):
            for col in range(self.tiles.shape[1]):
                if self.tiles[row][col] == 0:
                    return False
        return True

    def __no_more_moves(self):
        for row in range(1, self.tiles.shape[0]):
            for col in range(self.tiles.shape[1]):
                if self.tiles[row][col] == self.tiles[row - 1][col]:
                    return False
        for row in range(self.tiles.shape[0] - 2, -1, -1):
            for col in range(self.tiles.shape[1]):
                if self.tiles[row][col] == self.tiles[row + 1][col]:
                    return False
        for row in range(self.tiles.shape[0]):
            for col in range(self.tiles.shape[1] - 2, -1, -1):
                if self.tiles[row][col] == self.tiles[row][col + 1]:
                    return False
        for row in range(self.tiles.shape[0]):
            for col in range(1, self.tiles.shape[1]):
                if self.tiles[row][col] == self.tiles[row][col - 1]:
                    return False
        return True

    def is_game_over(self):
        if self.__full_board():
            return self.__no_more_moves()
        return False

    def new(self):
        self.tiles = np.zeros((ROWS, COLS))
        
        if self.mode == "4 x 4":
            self.tiles = np.zeros((4, 4))
        elif self.mode == "6 x 6":
            self.tiles = np.zeros((6, 6))
    
        self.score_manager.reset_score()
        self.generate_tiles(first=True)

    def run(self):
        global current_state  # Khai báo current_state là biến toàn cục ở đây
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            # Kiểm tra nếu pause_menu đang hoạt động; chỉ lắng nghe các sự kiện của menu tạm dừng nếu nó đang hoạt động
                if self.gui.pause_menu.active:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            result = self.gui.action_listener(event)
                            if result == 'MENU':
                                current_state = "MENU"
                                return
                            elif result is True:
                                self.new()
                else:  # Xử lý các sự kiện trò chơi chỉ khi menu tạm dừng không hoạt động
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.slide_tiles('UP')
                        elif event.key == pygame.K_DOWN:
                            self.slide_tiles('DOWN')
                        elif event.key == pygame.K_RIGHT:
                            self.slide_tiles('RIGHT')
                        elif event.key == pygame.K_LEFT:
                            self.slide_tiles('LEFT')
                    
                    # Nếu các ô được di chuyển và gộp lại, tạo ra một ô mới
                        if self.generate:
                            self.generate_tiles()
                            self.generate = False
                
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            result = self.gui.action_listener(event)
                            if result == 'MENU':
                                current_state = "MENU"
                                return
                            elif result is True:
                                self.new()

        # Hiển thị và cập nhật màn hình
            self.screen.fill(SCREEN_COLOR)
            self.draw_board()
            self.gui.menu.show()
            self.gui.pause_menu.show()
            self.gui.update_scores(self.score_manager.score, self.score_manager.best)

        # Kiểm tra kết thúc trò chơi và hiển thị menu game over nếu cần
            if self.is_game_over():
                self.gui.menu.active = True
        
            self.score_manager.check_highscore()
            self.gui.show_start()
            pygame.display.update()

        