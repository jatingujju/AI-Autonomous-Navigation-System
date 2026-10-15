class PerceptionModule:
    """
    Simulation-based perception module.
    Identifies obstacles using virtual grid data.
    """

    def __init__(self, rows, columns, obstacles):
        self.rows = rows
        self.columns = columns
        self.obstacles = set(obstacles)

    def get_obstacles(self):
        return {
            (row, column)
            for row, column in self.obstacles
            if 0 <= row < self.rows
            and 0 <= column < self.columns
        }

    def is_obstacle(self, position):
        return position in self.get_obstacles()