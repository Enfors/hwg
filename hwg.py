#!/usr/bin/env python3
#
# Hexagon War Game (working title) by Christer Enfors
#

import os, pygame, random, math

left_panel_x_size = 200
x_res = 1280
y_res = 800
panel_color = (144, 96, 64)
text_color  = (200, 160, 140)

all_directions = [ "above", "above_right", "below_right", "below",
                   "below_left", "above_left" ]

class Hexagon:
    def __init__(self, board, x_pos, y_pos):
        self.board = board
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.img_num = random.randint(0, 4)


    def draw(self, surface):
        surface.blit(self.board.images[self.img_num], self.query_screen_pos())


    def query_screen_pos(self):
        return self.board.query_h_screen_pos(self.x_pos, self.y_pos)        


    def __repr__(self):
        return "Hex(%d,%d)" % (self.x_pos, self.y_pos)



class Board:
    def __init__(self, cols = 10, rows = 10,
                 h_x_size = 37, h_y_size = 35, h_short_x_size = 29):
        
        self.rows = rows          # The number of hexagon rows
        self.cols = cols          # The number of hexagon columns

        self.h_x_size = h_x_size  # The x size of a hexagon
        self.h_y_size = h_y_size  # The y size of a hexagon

        self.h_short_x_size = h_short_x_size # The "short" x size

        self.x_size = ((h_short_x_size - 1) * (cols - 1)) + (h_x_size - 1)
        self.y_size = (((h_y_size - 1) * rows) + 1) + h_y_size / 2

        self.hexagons = []

        self.images = self.load_graphics("hexagons_37x35.png", 37, 35)

        for y in range(0, rows):
            row = []

            for x in range(0, cols):
                row.append(Hexagon(self, x, y))

            self.hexagons.append(row)

        self.img = pygame.Surface((self.x_size, self.y_size))
        self.draw(self.img)

        self.query_square_dist((0, 0), (0, 0))

        # x1 = 1
        # y1 = 0
        # print("Hexagons adjacent to %d,%d:" % (x1, y1))

        # for direction in all_directions:
        #     (adj_x, adj_y) = self.query_adjacent_h(x1, y1, direction)
        #     if (adj_x is not None and adj_y is not None):
        #         print("  %s: %d,%d" % (direction, adj_x, adj_y))
        #     else:
        #         print("  %s: (outside board)" % direction)
        
        # all_adj = self.query_all_adjacent_h(x1, y1)

        # print("List of adjacent hexagons: ")
        # for adj in all_adj:
        #     (adj_x, adj_y) = adj
        #     print("  (%d,%d) " % (adj_x, adj_y))


 
    def load_graphics(self, file_name, x_size, y_size):
        all_images = pygame.image.load("images%s%s" % (os.sep, file_name))
        all_images.convert_alpha()

        (img_x_size, img_y_size) = all_images.get_size()

        assert img_x_size % x_size == 0, "Incorrect x size"
        assert img_y_size % y_size == 0, "Incorrect y size"

        num_cols = int(img_x_size / x_size)
        num_rows = int(img_y_size / y_size)

        images = []

        for row in range(0, num_rows):
            for col in range(0, num_cols):
                new_hexagon = pygame.Surface((x_size, y_size))

                new_hexagon.blit(all_images, (0, 0),
                                 (col * x_size, row * y_size,
                                  (((col + 1) * x_size) - 1),
                                  (((row + 1) * y_size) - 1)))
                new_hexagon.convert()
                colorkey = new_hexagon.get_at((0, 0))
                new_hexagon.set_colorkey(colorkey, pygame.RLEACCEL)

                images.append(new_hexagon)

        return images


    def draw(self, surface):
        for hexagon in self.all_hexagons():
            hexagon.draw(surface)
        

    def all_hexagons(self):
        all_h = []

        for row in self.hexagons:
            for h in row:
                all_h.append(h)

        return all_h


    def query_h_screen_pos(self, x, y):
        """Returns the top left pixel of a hexagon on the screen."""
        screen_x_pos = (self.h_short_x_size - 1) * x

        screen_y_pos = (self.h_y_size - 1) * y

        if (x % 2 == 1):
            screen_y_pos += (self.h_y_size + 1) / 2 - 1

        return (screen_x_pos, screen_y_pos)


    def query_h_center_screen_pos(self, x, y):
        """Returns the center pixel of a hexagon on the screen."""
        (x, y) = self.query_h_screen_pos(x, y)

        x += (self.h_x_size + 1) / 2
        y += (self.h_y_size + 1) / 2

        return (x, y)


    def query_all_adjacent_h(self, x, y):
        """Returns all the hexagons adjacent to the hexagon at x, y."""
        all_adjacent = []

        for direction in all_directions:
            (adjacent_x, adjacent_y) = self.query_adjacent_h(x, y, direction)
            
            if (adjacent_x is not None and adjacent_y is not None):
                all_adjacent.append((adjacent_x, adjacent_y))

        return all_adjacent


    def query_adjacent_h(self, x, y, direction):
        """Returns the hexagon adjacent in the direction 'direction' to the
one at x, y."""

        assert direction in all_directions, "Invalid direction %s" % direction

        if (x % 2 == 0):
            even_x = True
        else:
            even_x = False

        if (direction == "above"):
            adjacent_x = x
            adjacent_y = y - 1

        elif (direction == "below"):
            adjacent_x = x
            adjacent_y = y + 1

        elif (direction == "above_right"):
            adjacent_x = x + 1
            if (even_x):
                adjacent_y = y - 1
            else:
                adjacent_y = y

        elif (direction == "below_right"):
            adjacent_x = x + 1
            if (even_x):
                adjacent_y = y
            else:
                adjacent_y = y + 1

        elif (direction == "below_left"):
            adjacent_x = x - 1
            if (even_x):
                adjacent_y = y
            else:
                adjacent_y = y + 1
        
        elif (direction == "above_left"):
            adjacent_x = x - 1
            if (even_x):
                adjacent_y = y - 1
            else:
                adjacent_y = y

        if (not self.query_is_valid_h(adjacent_x, adjacent_y)):
            return (None, None)

        return (adjacent_x, adjacent_y)


    def query_is_valid_h(self, x, y):
        """Returns True if the specified hexagon is on the board."""
        if (x < 0 or x > self.cols):
            return False
        if (y < 0 or y > self.rows):
            return False

        return True


    def query_square_dist(self, point1, point2):
        """Return the distinace between two points measured in a "square"
(not hexagons) system."""
        (x1, y1) = point1
        (x2, y2) = point2

        x_diff = x1 - x2
        y_diff = y1 - y2

        #print("Point1: %d,%d -- point2: %d,%d" % (x1, y1, x2, y2))
        #print("x_diff: %d -- y_diff: %d" % (x_diff, y_diff))

        dist = int(math.sqrt(x_diff * x_diff + y_diff * y_diff))

        #print("Dist: %d" % dist)
        return dist


    def query_h_center_point(self):
        """Return (x, y) representing the center point of a hexagon,
relative to itself (not the screen)."""
        return ((self.h_x_size + 1) / 2,
                (self.h_y_size + 1) / 2)



class Display:
    def __init__(self, screen, board, x_size, y_size):
        self.screen = screen       # The pygame screen
        self.board  = board        # The Board object
        self.x_size = x_size       # x resolution
        self.y_size = y_size       # y resolution

        self.board_x_pos = 0       # Top left pos of board currently displayed
        self.board_y_pos = 0       #

        self.max_board_x_pos = board.x_size - self.x_size + left_panel_x_size
        self.max_board_y_pos = board.y_size - self.y_size

        if self.max_board_x_pos < 0:
            self.max_board_x_pos = 0
        if self.max_board_y_pos < 0:
            self.max_board_y_pos = 0

        self.x_speed = 0           # current x scrolling speed
        self.y_speed = 0           # current y scrolling speed

        self.panel = pygame.Surface((left_panel_x_size, y_size))
        self.panel.fill(panel_color)
        font = pygame.font.SysFont("Courier New", 32)
        text = font.render("Hexagon", True, text_color, panel_color)
        self.panel.blit(text, (30, 25))
        text = font.render("War Game", True, text_color, panel_color)
        self.panel.blit(text, (20, 65))
        self.screen.blit(self.panel, (0, 0))
        

    def refresh(self, do_scroll_x = 0, do_scroll_y = 0,
                force = False):
        do_redraw = force

        if (do_scroll_x == -1):
            self.x_speed -= 6
        if (do_scroll_x == 1):
            self.x_speed += 6
        if (do_scroll_y == -1):
            self.y_speed -= 6
        if (do_scroll_y == 1):
            self.y_speed += 6

        if self.x_speed or self.y_speed:
            self.board_x_pos = self.scroll(self.x_speed,
                                           self.board_x_pos,
                                           self.max_board_x_pos)
            self.board_y_pos = self.scroll(self.y_speed,
                                           self.board_y_pos,
                                           self.max_board_y_pos)
            do_redraw = True
            
        
        self.x_speed = self.apply_friction(self.x_speed)
        self.y_speed = self.apply_friction(self.y_speed)

        if do_redraw:
            self.screen.blit(self.board.img, (left_panel_x_size, 0),
                             (self.board_x_pos, self.board_y_pos,
                              self.board_x_pos + 
                              self.x_size - left_panel_x_size,
                              self.board_y_pos + self.y_size))
            
        
    def scroll(self, speed, pos, max_pos):
        pos += (speed / 5)

        if (pos > max_pos):
            return max_pos
        elif (pos < 0):
            return 0
        else:
            return pos


    def apply_friction(self, speed):
        if (speed > 50):
            speed = 50
        if (speed < -50):
            speed = -50

        if (speed):   
            speed -= (speed / 15)

        if (speed > 0):
            speed -= 1
        if (speed < 0):
            speed += 1
            
        return speed


class Game:
    def __init__(self, x_size = x_res, y_size = y_res):
        screen = self.init_pygame(x_size, y_size)

        self.board = Board(60, 40)

        self.display = Display(screen, self.board, x_size, y_size)


    def init_pygame(self, x_size, y_size):
        pygame.init()

        screen = pygame.display.set_mode((x_size, y_size))
        pygame.display.set_caption("Hexagon war game")
        
        self.clock = pygame.time.Clock()

        return screen


    def start(self):
        running = True

        self.display.refresh(0, 0, force = True)

        do_scroll_x = 0
        do_scroll_y = 0
        
        while (running):
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        do_scroll_x = -1
                    elif event.key == pygame.K_d:
                        do_scroll_x = 1

                    if event.key == pygame.K_w:
                        do_scroll_y = -1
                    elif event.key == pygame.K_s:
                        do_scroll_y = 1

                elif event.type == pygame.KEYUP:
                    if (event.key in (pygame.K_a, pygame.K_d)):
                        do_scroll_x = 0
                    if (event.key in (pygame.K_w, pygame.K_s)):
                        do_scroll_y = 0
                        
            self.display.refresh(do_scroll_x, do_scroll_y)
            
            pygame.display.flip()



if __name__ == "__main__":
    game = Game()
    game.start()
