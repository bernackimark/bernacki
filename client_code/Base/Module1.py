# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from .Form1 import Module1
#
#    Module1.say_hello()
#

import pygame
import sys

pygame.init()


class Game:
    pg_white, pg_gray, pg_black = (255, 255, 255), (128, 128, 128), (0, 0, 0)
    pg_font = pygame.font.SysFont('noteworthy', 48)
    pg_font_2 = pygame.font.SysFont('noteworthy', 20)
    pg_font_apple_symbols = pygame.font.SysFont('applesymbols', 160)

    def __init__(self, play_up_to, desired_hands, hand_id, trick_number, leader, follower, trump):
        self.play_up_to = play_up_to
        self.desired_hands = desired_hands  # only needed in bot v bot simulations
        self.hand_id = hand_id  # only used right now in bot v bot simulations
        self.trick_number = trick_number
        self.leader = leader
        self.follower = follower
        self.trump = trump

    @staticmethod
    def draw_br(x, y, w, h):  # black rectangle
        pygame.draw.rect(pg_screen, Game.pg_black, (x, y, w, h))
        pygame.display.update()

    @staticmethod
    def pg_draw_bot():
        pg_screen.blit(BOT_ICON, (Game.get_center(BOT_ICON)[0], 0))
        pygame.display.update()

    @staticmethod
    def blit_text(surface, font_name, text, text_color, x, y):
        a = font_name.render(str(text), False, text_color)
        surface.blit(a, (x, y))

    @staticmethod
    def concat_2_items(i1, i2):
        the_string = str(i1) + str(i2)
        return the_string

    @staticmethod
    def get_center(the_object):
        if the_object == 0:  # passing in the number zero will return the middle of the screen
            object_w, object_h = 0, 0
        else:
            object_w, object_h = the_object.get_size()
        screen_w, screen_h = pygame.display.get_surface().get_size()
        return round((screen_w - object_w) / 2), round((screen_h - object_h) / 2)  # return tuple (x, y)


pygame.display.set_caption("Ackerman")
FPS = 60
fps_clock = pygame.time.Clock()
pg_col_count, pg_row_count, pg_unit = 14, 10, 50
pg_size = (pg_unit * pg_col_count, pg_unit * pg_row_count)
pg_screen = pygame.display.set_mode(pg_size)
BOT_ICON = pygame.transform.scale(pygame.image.load("face.png"), (1.6 * pg_unit, 1.6 * pg_unit))
game_over = False
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            pygame.quit(), sys.exit()

    # ---- START GAME -----
    Game.pg_draw_bot()


sys.exit()
