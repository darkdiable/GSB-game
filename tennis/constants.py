import pygame

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650
FPS = 60

COURT_TOP = 80
COURT_BOTTOM = 580
COURT_LEFT = 100
COURT_RIGHT = 800
COURT_WIDTH = COURT_RIGHT - COURT_LEFT
COURT_HEIGHT = COURT_BOTTOM - COURT_TOP

NET_Y = COURT_TOP + COURT_HEIGHT // 2
NET_HEIGHT = 40
NET_WIDTH = 6

SERVICE_LINE_TOP = COURT_TOP + 110
SERVICE_LINE_BOTTOM = COURT_BOTTOM - 110
CENTER_MARK_X = COURT_LEFT + COURT_WIDTH // 2
SERVICE_BOX_WIDTH = COURT_WIDTH // 2 - 30

PLAYER_SIZE = 40
PLAYER_START_X = CENTER_MARK_X
PLAYER_START_Y = COURT_BOTTOM - 60

NPC_START_X = CENTER_MARK_X
NPC_START_Y = COURT_TOP + 60

BALL_RADIUS = 8
BALL_SERVE_SPEED = 12
BALL_MAX_SPEED = 18
BALL_BOUNCE_DAMPING = 0.75

PLAYER_SPEED = 6
NPC_SPEED = 5.5
NPC_REACTION_DELAY = 3

SERVE_BOX_LEFT_TOP = (CENTER_MARK_X - SERVICE_BOX_WIDTH, SERVICE_LINE_TOP)
SERVE_BOX_RIGHT_TOP = (CENTER_MARK_X, SERVICE_LINE_TOP)
SERVE_BOX_LEFT_BOTTOM = (CENTER_MARK_X - SERVICE_BOX_WIDTH, NET_Y - 5)
SERVE_BOX_RIGHT_BOTTOM = (CENTER_MARK_X, NET_Y - 5)

SCORE_POINTS = ['0', '15', '30', '40', 'AD']

COLORS = {
    'court': (30, 144, 255),
    'court_line': (255, 255, 255),
    'net': (255, 255, 255),
    'net_post': (100, 100, 100),
    'player': (0, 128, 255),
    'player_shirt': (0, 128, 255),
    'player_shorts': (255, 255, 255),
    'npc': (255, 69, 0),
    'npc_shirt': (255, 69, 0),
    'npc_shorts': (255, 255, 255),
    'ball': (255, 255, 0),
    'ball_shadow': (0, 0, 0, 100),
    'referee': (50, 50, 50),
    'referee_shirt': (255, 255, 255),
    'referee_pants': (50, 50, 50),
    'text': (255, 255, 255),
    'text_violation': (255, 0, 0),
    'ui_bg': (0, 0, 0, 150),
    'background': (34, 139, 34),
    'court_outside': (34, 139, 34),
    'score_bg': (0, 0, 0, 180)
}

GAME_STATES = ['start', 'serve', 'playing', 'point_end', 'game_over']
VIOLATIONS = [
    '发球失误！',
    '双误！',
    '出界！',
    '触网！',
    '过网击球！',
    '发球踩线！'
]

pygame.font.init()

def get_chinese_font(size):
    font_paths = [
        '/System/Library/Fonts/STHeiti Medium.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
    ]
    for path in font_paths:
        try:
            font = pygame.font.Font(path, size)
            test_surface = font.render('测试', True, (255, 255, 255))
            if test_surface.get_width() > 30:
                return font
        except:
            pass

    font_names = ['stheitimedium', 'stheitilight', 'songti']
    for name in font_names:
        font = pygame.font.SysFont(name, size)
        test_surface = font.render('测试', True, (255, 255, 255))
        if test_surface.get_width() > 30:
            return font

    return pygame.font.SysFont(None, size)

FONT_SMALL = get_chinese_font(18)
FONT_MEDIUM = get_chinese_font(28)
FONT_LARGE = get_chinese_font(48)
FONT_VIOLATION = get_chinese_font(32)
