import pygame
import random
import math

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (236, 1, 90)
BLUE = (45, 197, 244)
PINK = (240, 99, 164)
YELLOW = (252, 238, 33)

# Initialize Pygame
pygame.init()

# Grid dimensions
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
        if random.uniform(0, 1) < 0.3:
            self.wall = True

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

# Create the grid
grid = [[Spot(i, j) for j in range(rows)] for i in range(cols)]

# Add neighbors to each spot
for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)

# Set start and end points
start, end = grid[7][30], grid[cols - 7][rows - 6]
start.wall = False
end.wall = False

# Open and closed sets
open_set, closed_set = [start], []

def remove_from_array(arr, elt):
    arr[:] = [spot for spot in arr if spot != elt]

def heuristic(a, b):
    return math.dist((a.i, a.j), (b.i, b.j))

def draw():
    screen.fill(BLUE)
    
    for i in range(cols):
        for j in range(rows):
            grid[i][j].show(WHITE)

    for spot in closed_set:
        spot.show(RED, 3)

    for spot in open_set:
        spot.show(PINK, 3)

    path = []
    temp = current
    path.append(temp)
    while temp.previous:
        path.append(temp.previous)
        temp = temp.previous

    for spot in path:
        pygame.draw.rect(screen, YELLOW, (spot.i * w, spot.j * h, w, h), 0, border_radius=5)

    pygame.draw.line(screen, YELLOW, (0, 0), (path[0].i * w + w / 2, path[0].j * h + h / 2), 3)
    pygame.draw.line(screen, YELLOW, (width, height), (path[-1].i * w + w / 2, path[-1].j * h + h / 2), 3)

    pygame.display.flip()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if open_set:
        # Best next option
        winner = 0
        for i in range(len(open_set)):
            if open_set[i].f < open_set[winner].f:
                winner = i
        current = open_set[winner]

        # Did I finish?
        if current == end:
            print("DONE!")
            running = False

        # Best option moves from openSet to closedSet
        remove_from_array(open_set, current)
        closed_set.append(current)

        # Check all the neighbors
        for neighbor in current.neighbors:
            # Valid next spot?
            if neighbor not in closed_set and not neighbor.wall:
                temp_g = current.g + heuristic(neighbor, current)

                # Is this a better path than before?
                new_path = False
                if neighbor in open_set:
                    if temp_g < neighbor.g:
                        neighbor.g = temp_g
                        new_path = True
                else:
                    neighbor.g = temp_g
                    new_path = True
                    open_set.append(neighbor)

                # Yes, it's a better path
                if new_path:
                    neighbor.h = heuristic(neighbor, end)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.previous = current
    else:
        print('No solution')
        running = False

    draw()

pygame.quit()
