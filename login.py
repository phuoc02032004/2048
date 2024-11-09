import pygame
import os
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from main import current_state, handle_main_menu_events, main_menu

# Khởi tạo Pygame
pygame.init()

# Cài đặt kích thước màn hình
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# Tên game
pygame.display.set_caption("Game Login")

# Màu sắc
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)  # Màu xanh lá cho nút "Login"

# Font chữ
font = pygame.font.Font(None, 32)

# Khởi tạo Firebase
cred = credentials.Certificate("project-5418815373818035308-firebase-adminsdk-ipz4g-3c1b1e9521.json")  # Thay thế bằng đường dẫn đến file JSON của bạn
firebase_admin.initialize_app(cred)
db = firestore.client()

# Hàm kiểm tra đăng nhập
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

# Hàm hiển thị text
def display_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Hàm hiển thị input box
def input_box(text, color, x, y, width, height, active=False):
    pygame.draw.rect(screen, color, (x, y, width, height), 2)
    if active:
        pygame.draw.rect(screen, color, (x, y, width, height), 2)
    else:
        pygame.draw.rect(screen, color, (x, y, width, height), 1)
    display_text(text, black, x + 5, y + 5)

# Hàm xử lý sự kiện
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
                        current_state = "MENU" # Thay đổi trạng thái về MENU
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
            elif back_button_rect.collidepoint(event.pos):  # Xử lý click nút Back
                current_state = "MENU"  # Thay đổi trạng thái về MENU
                return current_state
            elif login_button_rect.collidepoint(event.pos):
                username = username_input.text
                password = password_input.text
                if check_login(username, password):
                    print("Đăng nhập thành công!")
                    current_state = "MENU" # Thay đổi trạng thái về MENU
                    return current_state
                else:
                    print("Sai tên đăng nhập hoặc mật khẩu!")
                    error_message = font.render("Sai tên đăng nhập hoặc mật khẩu!", True, red)
                    screen.blit(error_message, (250, 350))

    return current_state


# Khởi tạo input box
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

# Tạo nút Back
back_button_rect = pygame.Rect(250, 300, 300, 40)  # Tạo rect cho nút Back
login_button_rect = pygame.Rect(250, 350, 300, 40)

# Hàm hiển thị màn hình đăng nhập
def show_login_screen(screen):
    screen.fill(white)

    # Hiển thị tiêu đề
    display_text("Đăng nhập", black, 300, 100)

    # Hiển thị input box
    username_input.draw()
    password_input.draw()

    # Vẽ nút Login
    pygame.draw.rect(screen, green, login_button_rect, 0, 5)
    display_text("Login", black, 350, 355)

    # Vẽ nút Back
    pygame.draw.rect(screen, green, back_button_rect, 0, 5)
    display_text("Back", black, 350, 305)

    pygame.display.flip()

# Hàm chính
def main():
    current_state = "LOGIN"  # Khởi tạo trạng thái là LOGIN
    while True:
        mouse = pygame.mouse.get_pos()
        
        # Xử lý sự kiện
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if current_state == "LOGIN":
                    current_state = handle_login_events(mouse, current_state)

        # Vẽ màn hình tương ứng với trạng thái hiện tại
        if current_state == "LOGIN":
            show_login_screen(screen)
        elif current_state == "MENU":
            current_state = "MENU"  # Trả về MENU
            main_menu()  # Gọi hàm main_menu

if __name__ == "__main__":
    main()