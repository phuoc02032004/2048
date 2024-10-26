import pygame
import sys
from constants import *
from logicgame import Game, ScoreManager, GUI 

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
text_setting_rect = text_setting.get_rect(center=(180 + 130 // 2, 250 + 55 // 2 + 70)) 
text_exit = smallfont.render('Exit', True, color)
text_exit_rect = text_exit.get_rect(center=(180 + 130 // 2, 320 + 55 // 2 + 70)) 

text_easy = smallfont.render('4 x 4', True, color)
text_easy_rect = text_easy.get_rect(center=(300 + 130 // 2, 180 + 55 // 2)) 
text_hard = smallfont.render('6 x 6', True, color)
text_hard_rect = text_hard.get_rect(center=(300 + 130 // 2, 250 + 55 // 2)) 

def handle_menu_events(screen, current_state, mode_selected, show_mode_menu):
    # Xử lý sự kiện trong menu
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if ev.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            button_width = 130
            button_x = 180
            button_y = 180
            # Nút Start
            if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + 50:
                if current_state == "MENU":
                    current_state = "GAME"
                    return current_state, mode_selected, show_mode_menu
            # Nút Mode
            button_y = 180 + 70
            if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + 50:
                show_mode_menu = not show_mode_menu
                return current_state, mode_selected, show_mode_menu
            # Nút Setting
            button_y = 250 + 70
            if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + 50:
                return current_state, mode_selected, show_mode_menu
            # Nút Exit
            button_y = 320 + 70
            if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + 50:
                pygame.quit()
                sys.exit()
            # Xử lý lựa chọn độ khó khi menu chế độ hiển thị
            if show_mode_menu:
                if text_easy_rect.collidepoint(mouse):
                    mode_selected = "4 x 4"
                    import constants_4x4  
                    globals().update(constants_4x4.__dict__)  # Cập nhật các hằng số
                    show_mode_menu = False
                    return current_state, mode_selected, show_mode_menu
                if text_hard_rect.collidepoint(mouse):
                    mode_selected = "6 x 6"
                    import constants_6x6  
                    globals().update(constants_6x6.__dict__)  # Cập nhật các hằng số
                    show_mode_menu = False
                    return current_state, mode_selected, show_mode_menu
    return current_state, mode_selected, show_mode_menu

def draw_menu(screen, show_mode_menu, mode_selected):
    # Vẽ giao diện menu
    screen.fill(SCREEN_COLOR)
    mouse = pygame.mouse.get_pos()
    button_width = 130
    button_x = 180
    button_y = 180

    # Vẽ nút Start
    if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + 50:
        pygame.draw.rect(screen, color_light, [button_x, button_y, button_width, 55])
    else:
        pygame.draw.rect(screen, color_dark, [button_x, button_y, button_width, 55])
    screen.blit(text_start, text_start_rect)

    # Vẽ nút Mode
    button_y = 180 + 70
    if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + 50:
        pygame.draw.rect(screen, color_light, [button_x, button_y, button_width, 55])
    else:
        pygame.draw.rect(screen, color_dark, [button_x, button_y, button_width, 55])
    screen.blit(text_mode, text_mode_rect)

    # Vẽ nút Setting
    button_y = 250 + 70
    if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + 50:
        pygame.draw.rect(screen, color_light, [button_x, button_y, button_width, 55])
    else:
        pygame.draw.rect(screen, color_dark, [button_x, button_y, button_width, 55])
    screen.blit(text_setting, text_setting_rect)

    # Vẽ nút Exit
    button_y = 320 + 70
    if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + 50:
        pygame.draw.rect(screen, color_light, [button_x, button_y, button_width, 55])
    else:
        pygame.draw.rect(screen, color_dark, [button_x, button_y, button_width, 55])
    screen.blit(text_exit, text_exit_rect)

    # Vẽ menu chế độ nếu show_mode_menu là True
    if show_mode_menu:
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 150))
        screen.blit(surface, (0, 0))
        
        # Nút Easy
        button_width = text_easy_rect.width + 20
        button_height = text_easy_rect.height + 10
        button_x = text_easy_rect.centerx - button_width // 2
        button_y = text_easy_rect.centery - button_height // 2
        if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + button_height:
            pygame.draw.rect(screen, color_light, [button_x, button_y, button_width, button_height])
        else:
            pygame.draw.rect(screen, color_dark, [button_x, button_y, button_width, button_height])
        screen.blit(text_easy, text_easy_rect)
        
        # Nút Hard
        button_width = text_hard_rect.width + 20
        button_height = text_hard_rect.height + 10
        button_x = text_hard_rect.centerx - button_width // 2
        button_y = text_hard_rect.centery - button_height // 2
        if button_x <= mouse[0] <= button_x + button_width and button_y <= mouse[1] <= button_y + button_height:
            pygame.draw.rect(screen, color_light, [button_x, button_y, button_width, button_height])
        else:
            pygame.draw.rect(screen, color_dark, [button_x, button_y, button_width, button_height])
        screen.blit(text_hard, text_hard_rect)
    
    pygame.display.update()

def main():
    # Hàm main điều khiển luồng của trò chơi
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
        if current_state == "MENU":
            current_state, mode_selected, show_mode_menu = handle_menu_events(screen, current_state, mode_selected, show_mode_menu)
            draw_menu(screen, show_mode_menu, mode_selected)
        elif current_state == "GAME":
            if game is None:
                game = Game(screen, mode_selected)
                for i in range(2):
                    game.generate_tiles(True)
            game.run()

if __name__ == "__main__":
    main()