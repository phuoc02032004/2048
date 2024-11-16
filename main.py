import pygame
import sys
from constants import *
from logicgame import Game, ScoreManager, GUI  # Đảm bảo ScoreManager được import
from pymongo import MongoClient
import bcrypt

# Kết nối với MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["database"]
users_collection = db["users"]
pygame.init()

# Tải âm thanh
pygame.mixer.init()  # Khởi tạo mixer cho âm thanh
BACKGROUND_MUSIC = pygame.mixer.Sound("background_music.mp3")
BUTTON_CLICK_SOUND = pygame.mixer.Sound("button_click.wav")
GAME_WIN_SOUND = pygame.mixer.Sound("game_win.mp3")
GAME_OVER_SOUND = pygame.mixer.Sound("game_over.mp3")

pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1, 0.0)

# Cài đặt màn hình trò chơi
screen = pygame.display.set_mode((720, 720))
pygame.display.set_caption('2048')

# Định nghĩa màu sắc và font chữ
BACKGROUND_COLOR = (242, 242, 218)
BUTTON_COLOR = (119, 110, 101)
HOVER_COLOR = (142, 121, 101)
TEXT_COLOR = (255, 255, 255)
font = pygame.font.SysFont('Corbel', 40, bold=True)

# Các nút và giao diện người dùng
text_start = font.render('Start', True, TEXT_COLOR)
text_setting = font.render('Setting', True, TEXT_COLOR)
text_exit = font.render('Exit', True, TEXT_COLOR)
text_easy = font.render('4 x 4', True, TEXT_COLOR)
text_hard = font.render('6 x 6', True, TEXT_COLOR)

button_width, button_height = 200, 60
start_button_rect = pygame.Rect(260, 250, button_width, button_height)
setting_button_rect = pygame.Rect(260, 340, button_width, button_height)
exit_button_rect = pygame.Rect(260, 430, button_width, button_height)
easy_button_rect = pygame.Rect(260, 250, button_width, button_height)
hard_button_rect = pygame.Rect(260, 340, button_width, button_height)

# Các biến cho màn hình đăng nhập
input_box_width, input_box_height = 400, 50
input_rect_user = pygame.Rect(160, 250, input_box_width, input_box_height)
input_rect_password = pygame.Rect(160, 330, input_box_width, input_box_height)
button_login_rect = pygame.Rect(260, 420, button_width, button_height)
button_register_rect = pygame.Rect(260, 510, button_width, button_height)

# Biến trạng thái cho các ô nhập liệu
active_input = None
user_text = ''
password_text = ''

def save_user_data(username, password):
    """Lưu thông tin đăng ký vào MongoDB."""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_data = {
        'username': username,
        'password': hashed_password.decode('utf-8'),
    }
    users_collection.insert_one(user_data)

def check_user_data(username, password):
    """Kiểm tra thông tin đăng nhập từ MongoDB."""
    user = users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
        return True
    return False

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

def draw_input_box(screen, rect, text_surface, is_active):
    color = (255, 215, 0) if is_active else (255, 255, 255)
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, (0, 0, 0), rect, 2)  # Vẽ viền
    screen.blit(text_surface, (rect.x + 10, rect.y + 10))

def draw_login_screen(screen):
    screen.fill(BACKGROUND_COLOR)
    mouse = pygame.mouse.get_pos()

    # Vẽ các ô nhập liệu và nút với hiệu ứng hover
    text_user = font.render('Username', True, TEXT_COLOR)
    text_password = font.render('Password', True, TEXT_COLOR)
    
    # Vẽ ô nhập username và password
    draw_input_box(screen, input_rect_user, font.render(user_text, True, (0, 0, 0)), active_input == 'user')
    draw_input_box(screen, input_rect_password, font.render(password_text, True, (0, 0, 0)), active_input == 'password')

    text_login = font.render('Login', True, TEXT_COLOR)
    draw_button(screen, button_login_rect, text_login, button_login_rect.collidepoint(mouse))

    text_register = font.render('Register', True, TEXT_COLOR)
    draw_button(screen, button_register_rect, text_register, button_register_rect.collidepoint(mouse))

    pygame.display.update()

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

def play_button_click_sound():
    BUTTON_CLICK_SOUND.play()

def play_game_over_sound():
    GAME_OVER_SOUND.play()

def play_game_win_sound():
    GAME_WIN_SOUND.play()

def handle_login_events(mouse, current_state):
    global active_input, user_text, password_text

    if button_login_rect.collidepoint(mouse):
        # Kiểm tra thông tin đăng nhập
        if check_user_data(user_text, password_text):
            print(f"Login successful! Welcome, {user_text}")
            play_button_click_sound()  # Phát âm thanh khi nhấn nút
            return "SELECT_MODE"
        else:
            print("Invalid username or password!")
            return "LOGIN"
    elif button_register_rect.collidepoint(mouse):
        # Lưu thông tin đăng ký vào file
        save_user_data(user_text, password_text)
        print(f"Registered successfully! Username: {user_text}")
        play_button_click_sound()  # Phát âm thanh khi nhấn nút
        return "LOGIN"
    
    # Kiểm tra sự kiện ô nhập liệu
    if input_rect_user.collidepoint(mouse):
        active_input = 'user'
    elif input_rect_password.collidepoint(mouse):
        active_input = 'password'
    else:
        active_input = None

    return current_state

def handle_main_menu_events(mouse, current_state):
    if start_button_rect.collidepoint(mouse):
        play_button_click_sound()  # Phát âm thanh khi nhấn nút
        return "LOGIN"  # Chuyển sang màn hình đăng nhập
    elif back_button_rect.collidepoint(mouse):
        return "MENU"
    elif setting_button_rect.collidepoint(mouse):
        return "SETTING"
    elif exit_button_rect.collidepoint(mouse):
        pygame.quit()
        sys.exit()
    return current_state

def handle_select_mode_events(mouse, mode_selected):
    if easy_button_rect.collidepoint(mouse):
        mode_selected = "4 x 4"
        play_button_click_sound()  # Phát âm thanh khi nhấn nút
        return "GAME", mode_selected
    elif hard_button_rect.collidepoint(mouse):
        mode_selected = "6 x 6"
        play_button_click_sound()  # Phát âm thanh khi nhấn nút
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
    global active_input, user_text, password_text

    pygame.init()
    screen = pygame.display.set_mode((720, 720))
    pygame.display.set_caption('2048')

    current_state = "MENU"
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
                elif current_state == "LOGIN":
                    current_state = handle_login_events(mouse, current_state)
                elif current_state == "SELECT_MODE":
                    current_state, mode_selected = handle_select_mode_events(mouse, mode_selected)
                elif current_state == "SETTING":
                    current_state = handle_setting_events(mouse, current_state)
            elif ev.type == pygame.KEYDOWN:
                # Xử lý sự kiện bàn phím khi người dùng nhập văn bản
                if active_input == 'user':
                    if ev.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]  # Xóa ký tự cuối
                    else:
                        user_text += ev.unicode
                elif active_input == 'password':
                    if ev.key == pygame.K_BACKSPACE:
                        password_text = password_text[:-1]  # Xóa ký tự cuối
                    else:
                        password_text += ev.unicode

        if current_state == "MENU":
            draw_main_menu(screen)
        elif current_state == "LOGIN":
            draw_login_screen(screen)
        elif current_state == "SELECT_MODE":
            draw_select_mode(screen)
        elif current_state == "SETTING":
            draw_setting_menu(screen)
        elif current_state == "GAME":
            game = Game(screen, mode_selected)
            for i in range(2):
                game.generate_tiles(True)
            game.run()
            current_state = "MENU"
            play_game_over_sound()  # Phát âm thanh khi kết thúc trò chơi

if __name__ == "__main__":
    main()
