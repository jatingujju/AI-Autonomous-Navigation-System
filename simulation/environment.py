
import os
import sys
import pygame

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
sys.path.insert(0, PROJECT_ROOT)

from src.path_planning import astar
from src.perception import PerceptionModule


class GridEnvironment:
    def __init__(self):
        pygame.init()

        self.cell_size = 40
        self.columns = 15
        self.rows = 12

        self.width = self.columns * self.cell_size
        self.height = self.rows * self.cell_size

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )
        pygame.display.set_caption(
            "AI-Based Autonomous Navigation System"
        )

        self.clock = pygame.time.Clock()

        self.start = (1, 1)
        self.goal = (10, 13)

        # Obstacles in the virtual environment
        self.obstacles = {
            (2, 3), (3, 3), (4, 3),
            (5, 3), (6, 3),
            (6, 5), (6, 6), (6, 7),
            (3, 8), (4, 8), (5, 8),
            (7, 10), (8, 10), (9, 10),
            (2, 12), (3, 12), (4, 12)
        }

        # Perception module identifies occupied grid cells
        self.perception = PerceptionModule(
            rows=self.rows,
            columns=self.columns,
            obstacles=self.obstacles
        )

        self.obstacles = self.perception.get_obstacles()

        # A* calculates a path around the obstacles
        self.path = astar(
            start=self.start,
            goal=self.goal,
            obstacles=self.obstacles,
            rows=self.rows,
            columns=self.columns
        )

        self.background_color = (245, 245, 245)
        self.grid_color = (200, 200, 200)
        self.obstacle_color = (50, 50, 50)
        self.start_color = (40, 180, 80)
        self.goal_color = (220, 60, 60)
        self.path_color = (70, 140, 240)
        self.robot_color = (255, 190, 0)

        self.robot_position = self.start
        self.path_index = 0
        self.move_timer = 0
        self.move_interval = 250
        self.finished = False

    def draw_cell(self, position, color):
        row, column = position

        rectangle = pygame.Rect(
            column * self.cell_size,
            row * self.cell_size,
            self.cell_size,
            self.cell_size
        )

        pygame.draw.rect(self.screen, color, rectangle)
        pygame.draw.rect(
            self.screen,
            self.grid_color,
            rectangle,
            1
        )

    def move_robot(self, elapsed_time):
        if not self.path or self.finished:
            return

        self.move_timer += elapsed_time

        if self.move_timer >= self.move_interval:
            self.move_timer = 0

            if self.path_index < len(self.path) - 1:
                self.path_index += 1
                self.robot_position = self.path[self.path_index]

                print("Robot position:", self.robot_position)

            if self.robot_position == self.goal:
                self.finished = True
                print("Destination reached successfully.")

    def draw(self):
        self.screen.fill(self.background_color)

        # Draw the grid
        for row in range(self.rows):
            for column in range(self.columns):
                self.draw_cell(
                    (row, column),
                    self.background_color
                )

        # Draw the calculated route
        for position in self.path:
            if position not in (self.start, self.goal):
                self.draw_cell(position, self.path_color)

        # Draw obstacles
        for obstacle in self.obstacles:
            self.draw_cell(obstacle, self.obstacle_color)

        # Draw start, destination, and moving agent
        self.draw_cell(self.start, self.start_color)
        self.draw_cell(self.goal, self.goal_color)
        self.draw_cell(self.robot_position, self.robot_color)

        pygame.display.flip()

    def run(self):
        if self.path:
            print("Perception module initialized successfully.")
            print("A* path found successfully.")
            print("Number of moves:", len(self.path) - 1)
        else:
            print("No valid path found.")
            pygame.quit()
            return

        running = True

        while running:
            elapsed_time = self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.move_robot(elapsed_time)
            self.draw()

        pygame.quit()


if __name__ == "__main__":
    environment = GridEnvironment()
    environment.run()
