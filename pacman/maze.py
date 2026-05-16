from constants import *
import pygame

MAP_LAYOUT = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#o####.#####.##.#####.####o#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "     #.##### ## #####.#     ",
    "     #.##          ##.#     ",
    "     #.## ###--### ##.#     ",
    "######.## #      # ##.######",
    "      .   #  GG  #   .      ",
    "######.## #      # ##.######",
    "     #.## ######## ##.#     ",
    "     #.##          ##.#     ",
    "     #.## ######## ##.#     ",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#o..##.......P .......##..o#",
    "###.##.##.########.##.##.###",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################",
]


class Maze:
    def __init__(self):
        self.layout = [list(row) for row in MAP_LAYOUT]
        self.pellets = []
        self.power_pellets = []
        self.walls = []
        self.ghost_house = []
        self.pacman_start = (0, 0)
        self.ghost_starts = []
        self._parse_layout()

    def _parse_layout(self):
        for row in range(len(self.layout)):
            for col in range(len(self.layout[row])):
                cell = self.layout[row][col]
                x = col * CELL_SIZE + CELL_SIZE // 2
                y = row * CELL_SIZE + CELL_SIZE // 2
                if cell == WALL:
                    self.walls.append((col, row))
                elif cell == PELLET:
                    self.pellets.append((x, y))
                elif cell == POWER_PELLET:
                    self.power_pellets.append((x, y))
                elif cell == GHOST_HOUSE:
                    self.ghost_house.append((col, row))
                elif cell == PACMAN_START:
                    self.pacman_start = (x, y)
                elif cell == GHOST_START:
                    self.ghost_starts.append((x, y))

    def is_wall(self, col, row):
        if col < 0 or col >= COLS or row < 0 or row >= ROWS:
            return True
        if row >= 0 and row < len(self.layout) and col >= 0 and col < len(self.layout[row]):
            return self.layout[row][col] == WALL
        return True

    def is_ghost_house(self, col, row):
        if row >= 0 and row < len(self.layout) and col >= 0 and col < len(self.layout[row]):
            return self.layout[row][col] == GHOST_HOUSE
        return False

    def remove_pellet(self, x, y):
        self.pellets = [p for p in self.pellets if p != (x, y)]

    def remove_power_pellet(self, x, y):
        self.power_pellets = [p for p in self.power_pellets if p != (x, y)]

    def get_cell(self, x, y):
        col = int(x // CELL_SIZE)
        row = int(y // CELL_SIZE)
        return col, row

    def draw(self, screen):
        for row in range(len(self.layout)):
            for col in range(len(self.layout[row])):
                if self.layout[row][col] == WALL:
                    pygame.draw.rect(screen, BLUE,
                                     (col * CELL_SIZE + 1, row * CELL_SIZE + 1,
                                      CELL_SIZE - 2, CELL_SIZE - 2), 1)

        for px, py in self.pellets:
            pygame.draw.circle(screen, WHITE, (int(px), int(py)), PELLET_SIZE)

        for px, py in self.power_pellets:
            pygame.draw.circle(screen, WHITE, (int(px), int(py)), POWER_PELLET_SIZE)

    def all_pellets_eaten(self):
        return len(self.pellets) == 0 and len(self.power_pellets) == 0
