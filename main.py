import pygame
import sys
from constants import *
from logicgame import Game, ScoreManager, GUI

pygame.init()
res = (720, 720)
screen = pygame.display.set_mode(res)
pygame.display.set_caption('2048')

# Định nghĩa màu sắc
BACKGROUND_COLOR = (242, 242, 218)
BUTTON_COLOR = (119, 110, 101)
HOVER_COLOR = (142, 121, 101)
TEXT_COLOR = (255, 255, 255)

# Font chữ
font = pygame.font.SysFont('Corbel', 40, bold=True)
text_start = font.render('Start', True, TEXT_COLOR)
text_setting = font.render('Setting', True, TEXT_COLOR)
text_exit = font.render('Exit', True, TEXT_COLOR)
text_easy = font.render('4 x 4', True, TEXT_COLOR)
text_hard = font.render('6 x 6', True, TEXT_COLOR)

# Kích thước và vị trí nút
button_width, button_height = 200, 60
start_button_rect = pygame.Rect(260, 250, button_width, button_height)
setting_button_rect = pygame.Rect(260, 340, button_width, button_height)
exit_button_rect = pygame.Rect(260, 430, button_width, button_height)
easy_button_rect = pygame.Rect(260, 250, button_width, button_height)
hard_button_rect = pygame.Rect(260, 340, button_width, button_height)

def draw_button(screen, rect, text_surface, is_hovered):
    color = HOVER_COLOR if is_hovered else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=15)
    screen.blit(text_surface, text_surface.get_rect(center=rect.center))

def draw_main_menu(screen):
    screen.fill(BACKGROUND_COLOR)
    mouse = pygame.mouse.get_pos()

    # Vẽ các nút với hiệu ứng hover
    draw_button(screen, start_button_rect, text_start, start_button_rect.collidepoint(mouse))
    draw_button(screen, setting_button_rect, text_setting, setting_button_rect.collidepoint(mouse))
    draw_button(screen, exit_button_rect, text_exit, exit_button_rect.collidepoint(mouse))

    pygame.display.update()

def draw_select_mode(screen):
    screen.fill(BACKGROUND_COLOR)
    mouse = pygame.mouse.get_pos()

    # Vẽ các nút chọn chế độ với hiệu ứng hover
    draw_button(screen, easy_button_rect, text_easy, easy_button_rect.collidepoint(mouse))
    draw_button(screen, hard_button_rect, text_hard, hard_button_rect.collidepoint(mouse))

    pygame.display.update()

def handle_main_menu_events(mouse, current_state):
    # Xử lý sự kiện cho menu chính
    if start_button_rect.collidepoint(mouse):
        return "SELECT_MODE"  # Chuyển sang màn hình chọn chế độ
    elif setting_button_rect.collidepoint(mouse):
        # Thêm xử lý cài đặt nếu cần
        return "MENU"
    elif exit_button_rect.collidepoint(mouse):
        pygame.quit()
        sys.exit()
    return current_state

def handle_select_mode_events(mouse, mode_selected):
    # Xử lý sự kiện cho màn hình chọn chế độ
    if easy_button_rect.collidepoint(mouse):
        mode_selected = "4 x 4"
        return "GAME", mode_selected
    elif hard_button_rect.collidepoint(mouse):
        mode_selected = "6 x 6"
        return "GAME", mode_selected
    return "SELECT_MODE", mode_selected

def main():
    pygame.init()
    screen = pygame.display.set_mode((720, 720))
    pygame.display.set_caption('2048')

    current_state = "MENU"
    mode_selected = None

    while True:
        mouse = pygame.mouse.get_pos()
        
        # Xử lý sự kiện
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if current_state == "MENU":
                    current_state = handle_main_menu_events(mouse, current_state)
                elif current_state == "SELECT_MODE":
                    current_state, mode_selected = handle_select_mode_events(mouse, mode_selected)

        # Vẽ màn hình tương ứng với trạng thái hiện tại
        if current_state == "MENU":
            draw_main_menu(screen)
        elif current_state == "SELECT_MODE":
            draw_select_mode(screen)
        elif current_state == "GAME":
            game = Game(screen, mode_selected)
            for i in range(2):
                game.generate_tiles(True)
            game.run()
            current_state = "MENU"

if __name__ == "__main__":
    main()
