import pygame
import os
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from logicgame import Game

pygame.init()

width = 800
height = 600
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Game Login")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

font = pygame.font.Font(None, 32)

cred = credentials.Certificate("project-5418815373818035308-firebase-adminsdk-ipz4g-3c1b1e9521.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def check_login(username, password):
    user_ref = db.collection('users').document(username)
    user = user_ref.get()
    if user.exists:
        if user.to_dict()["password"] == password:
            return True
        else:
            return False
    else:
        return False

def display_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def input_box(text, color, x, y, width, height, active=False):
    pygame.draw.rect(screen, color, (x, y, width, height), 2)
    if active:
        pygame.draw.rect(screen, color, (x, y, width, height), 2)
    else:
        pygame.draw.rect(screen, color, (x, y, width, height), 1)
    display_text(text, black, x + 5, y + 5)

def handle_login_events(mouse, current_state):
    global username_input, password_input, username, password
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if username_input.active:
                    password_input.active = True
                    username_input.active = False
                else:
                    username = username_input.text
                    password = password_input.text
                    if check_login(username, password):
                        print("Đăng nhập thành công!")
                        current_state = "MENU"
                        return current_state
                    else:
                        print("Sai tên đăng nhập hoặc mật khẩu!")
                        error_message = font.render("Sai tên đăng nhập hoặc mật khẩu!", True, red)
                        screen.blit(error_message, (250, 350))
            elif event.key == pygame.K_BACKSPACE:
                if username_input.active:
                    username_input.text = username_input.text[:-1]
                elif password_input.active:
                    password_input.text = password_input.text[:-1]
            else:
                if username_input.active:
                    username_input.text += event.unicode
                elif password_input.active:
                    password_input.text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if username_input.rect.collidepoint(event.pos):
                username_input.active = True
                password_input.active = False
            elif password_input.rect.collidepoint(event.pos):
                username_input.active = False
                password_input.active = True
            elif back_button_rect.collidepoint(event.pos):
                current_state = "MENU"
                return current_state
            elif login_button_rect.collidepoint(event.pos):
                username = username_input.text
                password = password_input.text
                if check_login(username, password):
                    print("Đăng nhập thành công!")
                    current_state = "MENU"
                    return current_state
                else:
                    print("Sai tên đăng nhập hoặc mật khẩu!")
                    error_message = font.render("Sai tên đăng nhập hoặc mật khẩu!", True, red)
                    screen.blit(error_message, (250, 350))

    return current_state

class InputBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = black
        self.text = ""
        self.active = False

    def draw(self):
        input_box(self.text, self.color, self.rect.x, self.rect.y, self.rect.width, self.rect.height, self.active)

username_input = InputBox(250, 200, 300, 40)
password_input = InputBox(250, 250, 300, 40)

back_button_rect = pygame.Rect(250, 300, 300, 40)
login_button_rect = pygame.Rect(250, 350, 300, 40)

def show_login_screen(screen):
    global current_state
    while current_state == "LOGIN":
        mouse = pygame.mouse.get_pos()
        screen.fill(white)
        display_text("Đăng nhập", black, 300, 100)
        username_input.draw()
        password_input.draw()
        pygame.draw.rect(screen, green, login_button_rect, 0, 5)
        display_text("Login", black, 350, 355)
        pygame.draw.rect(screen, green, back_button_rect, 0, 5)
        display_text("Back", black, 350, 305)
        
        current_state = handle_login_events(mouse, current_state)

        pygame.display.flip()

# Constants and functions for 2048 game

# Define colors
BACKGROUND_COLOR = (242, 242, 218)
BUTTON_COLOR = (119, 110, 101)
HOVER_COLOR = (142, 121, 101)
TEXT_COLOR = (255, 255, 255)
SLIDER_COLOR = (178, 171, 160)

# Define fonts
font = pygame.font.SysFont('Corbel', 40, bold=True)
font_small = pygame.font.SysFont('Corbel', 30, bold=True)
text_start = font.render('Start', True, TEXT_COLOR)
text_setting = font.render('Setting', True, TEXT_COLOR)
text_exit = font.render('Exit', True, TEXT_COLOR)
text_easy = font.render('4 x 4', True, TEXT_COLOR)
text_hard = font.render('6 x 6', True, TEXT_COLOR)
text_music_on = font.render('Music On', True, TEXT_COLOR)
text_music_off = font.render('Music Off', True, TEXT_COLOR)
text_back = font.render('Back', True, TEXT_COLOR)
text_volume = font_small.render('Volume', True, TEXT_COLOR)
text_login = font.render('Login', True, TEXT_COLOR)

# Define button sizes and positions
button_width, button_height = 200, 60
start_button_rect = pygame.Rect(260, 250, button_width, button_height)
setting_button_rect = pygame.Rect(260, 340, button_width, button_height)
exit_button_rect = pygame.Rect(260, 430, button_width, button_height)
easy_button_rect = pygame.Rect(260, 250, button_width, button_height)
hard_button_rect = pygame.Rect(260, 340, button_width, button_height)
music_button_rect = pygame.Rect(260, 250, button_width, button_height)
back_button_rect = pygame.Rect(260, 430, button_width, button_height)
login_button_rect = pygame.Rect(260, 520, button_width, button_height)

# Initialize music
pygame.mixer.init()
music = pygame.mixer.music
music.load("Sound.mp3")
music.set_volume(0.5)
music.play(-1)

# Music state
music_on = True
volume = 0.5

def draw_button(screen, rect, text_surface, is_hovered):
    color = HOVER_COLOR if is_hovered else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=15)
    screen.blit(text_surface, text_surface.get_rect(center=rect.center))

def draw_main_menu(screen):
    screen.fill(BACKGROUND_COLOR)
    mouse = pygame.mouse.get_pos()
    draw_button(screen, start_button_rect, text_start, start_button_rect.collidepoint(mouse))
    draw_button(screen, setting_button_rect, text_setting, setting_button_rect.collidepoint(mouse))
    draw_button(screen, exit_button_rect, text_exit, exit_button_rect.collidepoint(mouse))
    draw_button(screen, login_button_rect, text_login, login_button_rect.collidepoint(mouse))
    draw_button(screen, back_button_rect, text_back, back_button_rect.collidepoint(mouse))
    pygame.display.update()

def main_menu():
    draw_main_menu(screen)
    pygame.display.update()

def draw_select_mode(screen):
    screen.fill(BACKGROUND_COLOR)
    mouse = pygame.mouse.get_pos()
    draw_button(screen, easy_button_rect, text_easy, easy_button_rect.collidepoint(mouse))
    draw_button(screen, hard_button_rect, text_hard, hard_button_rect.collidepoint(mouse))
    pygame.display.update()

def draw_setting_menu(screen):
    screen.fill(BACKGROUND_COLOR)
    mouse = pygame.mouse.get_pos()
    if music_on:
        music_text = text_music_on
    else:
        music_text = text_music_off
    draw_button(screen, music_button_rect, music_text, music_button_rect.collidepoint(mouse))
    slider_rect = pygame.Rect(260, 340, button_width, 20)
    slider_x = slider_rect.x + int(volume * slider_rect.width)
    slider_button_rect = pygame.Rect(slider_x - 10, slider_rect.y - 10, 20, 40)
    pygame.draw.rect(screen, SLIDER_COLOR, slider_rect)
    pygame.draw.rect(screen, BUTTON_COLOR, slider_button_rect, border_radius=5)
    draw_button(screen, back_button_rect, text_back, back_button_rect.collidepoint(mouse))
    pygame.display.update()

current_state = "MENU" 

def handle_main_menu_events(mouse, current_state):
    if start_button_rect.collidepoint(mouse):
        return "SELECT_MODE"
    elif setting_button_rect.collidepoint(mouse):
        return "SETTING"
    elif exit_button_rect.collidepoint(mouse):
        pygame.quit()
        sys.exit()
    elif login_button_rect.collidepoint(mouse):
        show_login_screen(screen)
        return "LOGIN"
    elif back_button_rect.collidepoint(mouse):
        return "MENU"
    return current_state

def handle_select_mode_events(mouse, mode_selected):
    if easy_button_rect.collidepoint(mouse):
        mode_selected = "4 x 4"
        return "GAME", mode_selected
    elif hard_button_rect.collidepoint(mouse):
        mode_selected = "6 x 6"
        return "GAME", mode_selected
    return "SELECT_MODE", mode_selected

def handle_setting_events(mouse, current_state):
    global music_on, volume
    if music_button_rect.collidepoint(mouse):
        music_on = not music_on
        if music_on:
            music.unpause()
        else:
            music.pause()
    elif back_button_rect.collidepoint(mouse):
        return "MENU"
    slider_rect = pygame.Rect(260, 340, button_width, 20)
    if slider_rect.collidepoint(mouse):
        volume = (mouse[0] - slider_rect.x) / slider_rect.width
        volume = max(0, min(volume, 1))
        music.set_volume(volume)
    return current_state

def main():
    global current_state
    mode_selected = None
    while True:
        mouse = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if current_state == "MENU":
                    current_state = handle_main_menu_events(mouse, current_state)
                elif current_state == "SELECT_MODE":
                    current_state, mode_selected = handle_select_mode_events(mouse, mode_selected)
                elif current_state == "SETTING":
                    current_state = handle_setting_events(mouse, current_state)
                elif current_state == "LOGIN":
                    show_login_screen(screen)
                    # current_state = handle_login_events(mouse, current_state)  # Already handled in show_login_screen
                elif current_state == "GAME":
                    game = Game(screen, mode_selected)
                    for i in range(2):
                        game.generate_tiles(True)
                    game.run()
                    current_state = "MENU"

        if current_state == "MENU":
            draw_main_menu(screen)
        elif current_state == "SELECT_MODE":
            draw_select_mode(screen)
        elif current_state == "SETTING":
            draw_setting_menu(screen)
        elif current_state == "LOGIN":
            show_login_screen(screen)
        elif current_state == "GAME":
            game = Game(screen, mode_selected)
            for i in range(2):
                game.generate_tiles(True)
            game.run()
            current_state = "MENU"

if __name__ == "__main__":
    main()