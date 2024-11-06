# Determine Board Size
BOARD_SIZE = 4  # Set to 4 for 4x4 or 6 for 6x6

# SIZE
if BOARD_SIZE == 4:
    WIDTH, HEIGHT = 600, 800
    BOARD_WIDTH, BOARD_HEIGHT = 280, 280
    COLS, ROWS = 4, 4
    GAP = 8
    TILE_SIZE = (280 - 5 * GAP) // 4
else:
    WIDTH, HEIGHT = 600, 800
    BOARD_WIDTH, BOARD_HEIGHT = 330, 330
    COLS, ROWS = 6, 6
    GAP = 6
    TILE_SIZE = (360 - 7 * GAP) // 6

XSHIFT, XSHIFT2, XSHIFT3 = 100, 197, 264
YSHIFT, YSHIFT2, YSHIFT3 = 20, 85, 144

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCREEN_COLOR = (249, 246, 235)
BOARD_COLOR = (173, 157, 143)

color = (255, 255, 255)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)

# MENU
GAMEOVER_LBL_COLOR = (119, 111, 102)
TRANSPARENT_ALPHA = 210

# TILE COLORS
TILES_COLORS = {
    0: (194, 178, 166),
    2: (233, 221, 209),
    4: (232, 217, 189),
    8: (236, 161, 101),
    16: (241, 130, 80),
    32: (239, 100, 77),
    64: (240, 69, 45),
    128: (230, 197, 94),
    256: (227, 190, 78),
    512: (230, 189, 64),
    1024: (233, 185, 49),
    2048: (233, 187, 32),
    4096: (35, 32, 29),
    8192: (35, 32, 29),
}

# LABEL COLORS
LBLS_COLORS = {
    0: (194, 178, 166),
    2: (99, 91, 82),
    4: (99, 91, 82),
    8: WHITE,
    16: WHITE,
    32: WHITE,
    64: WHITE,
    128: WHITE,
    256: WHITE,
    512: WHITE,
    1024: WHITE,
    2048: WHITE,
    4096: WHITE,
    8192: WHITE,
}
