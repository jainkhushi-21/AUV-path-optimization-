import pygame
import random
import math

from aco import heuristic



# Define colors
WHITE = (255, 255, 255)
RED = (236, 1, 90)
BLUE = (45, 197, 244)
PINK = (240, 99, 164)
YELLOW = (252, 238, 33)

# Initialize Pygame
pygame.init()

# Set up grid dimensions
cols, rows = 50, 50
width, height = 800, 800
w, h = width // cols, height // rows

# Create the screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('A* Algorithm')

class Spot:
    def __init__(self, i, j):
        self.i, self.j = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.previous = None
        self.wall = False

    def show(self, color, alpha=1):
        pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), 0 if not self.wall else 1, border_radius=5)
        pygame.draw.line(screen, WHITE, (self.i * w, self.j * h), ((self.i + 1) * w, self.j * h), 1)
        pygame.draw.line(screen, WHITE, ((self.i + 1) * w, self.j * h), ((self.i + 1) * w, (self.j + 1) * h), 1)
        pygame.draw.line(screen, WHITE, ((self.i + 1) * w, (self.j + 1) * h), (self.i * w, (self.j + 1) * h), 1)
        pygame.draw.line(screen, WHITE, (self.i * w, (self.j + 1) * h), (self.i * w, self.j * h), 1)

    def add_neighbors(self, grid):
        i, j = self.i, self.j
        if i < cols - 1:
            self.neighbors.append(grid[i + 1][j])
        if i > 0:
            self.neighbors.append(grid[i - 1][j])
        if j < rows - 1:
            self.neighbors.append(grid[i][j + 1])
        if j > 0:
            self.neighbors.append(grid[i][j - 1])

def heuristic(a, b):
    return math.dist((a.i, a.j), (b.i, b.j))

def find_path(start, end):
    open_set, closed_set = [start], []
    start.g = 0
    start.h = heuristic(start, end)
    start.f = start.g + start.h

    while open_set:
        current = min(open_set, key=lambda spot: spot.f)

        if current == end:
            # Reconstruct the path
            path = []
            temp = current
            while temp:
                path.insert(0, temp)
                temp = temp.previous
            return path

        open_set.remove(current)
        closed_set.append(current)

        for neighbor in current.neighbors:
            if neighbor in closed_set or neighbor.wall:
                continue

            temp_g = current.g + heuristic(neighbor, current)

            if neighbor not in open_set or temp_g < neighbor.g:
                neighbor.g = temp_g
                neighbor.h = heuristic(neighbor, end)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.previous = current

                if neighbor not in open_set:
                    open_set.append(neighbor)

    # No path found
    return []

# Set up grid, start, and end points
grid = [[Spot(i, j) for j in range(rows)] for i in range(cols)]
for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)

start, end = None, None
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                clicked_spot = grid[mouse_pos[0] // w][mouse_pos[1] // h]
                if not start:
                    start = clicked_spot
                    start.wall = False
                elif not end and clicked_spot != start:
                    end = clicked_spot
                    end.wall = False
                else:
                    clicked_spot.wall = True  # Set as wall
            elif event.button == 3:  # Right mouse button
                mouse_pos = pygame.mouse.get_pos()
                clicked_spot = grid[mouse_pos[0] // w][mouse_pos[1] // h]
                clicked_spot.wall = not clicked_spot.wall  # Toggle wall status

    screen.fill(BLUE)

    for i in range(cols):
        for j in range(rows):
            grid[i][j].show(WHITE if not grid[i][j].wall else BLUE)

    if start:
        start.show(RED)
    if end:
        end.show(RED)

    if start and end:
        path = find_path(start, end)
        for spot in path:
            pygame.draw.rect(screen, YELLOW, (spot.i * w, spot.j * h, w, h), 0, border_radius=5)
        pygame.draw.line(screen, YELLOW, (start.i * w + w / 2, start.j * h + h / 2), (end.i * w + w / 2, end.j * h + h / 2), 3)

    pygame.display.flip()

pygame.quit()

