
import heapq


def heuristic(current, goal):
    """Calculate Manhattan distance between two grid cells."""
    row_distance = abs(current[0] - goal[0])
    column_distance = abs(current[1] - goal[1])

    return row_distance + column_distance


def get_neighbors(position, rows, columns):
    """Return valid cells in the four adjacent directions."""
    row, column = position

    possible_neighbors = [
        (row - 1, column),
        (row + 1, column),
        (row, column - 1),
        (row, column + 1)
    ]

    return [
        neighbor
        for neighbor in possible_neighbors
        if 0 <= neighbor[0] < rows
        and 0 <= neighbor[1] < columns
    ]


def reconstruct_path(came_from, current):
    """Reconstruct the path from goal back to start."""
    path = [current]

    while current in came_from:
        current = came_from[current]
        path.append(current)

    path.reverse()
    return path


def astar(start, goal, obstacles, rows, columns):
    """Find a shortest path while avoiding obstacle cells."""

    if start in obstacles or goal in obstacles:
        return []

    open_set = []
    heapq.heappush(
        open_set,
        (heuristic(start, goal), start)
    )

    came_from = {}
    g_score = {start: 0}
    visited = set()

    while open_set:
        _, current = heapq.heappop(open_set)

        if current in visited:
            continue

        if current == goal:
            return reconstruct_path(came_from, current)

        visited.add(current)

        for neighbor in get_neighbors(
            current, rows, columns
        ):
            if neighbor in obstacles:
                continue

            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score.get(
                neighbor, float("inf")
            ):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score

                f_score = (
                    tentative_g_score
                    + heuristic(neighbor, goal)
                )

                heapq.heappush(
                    open_set,
                    (f_score, neighbor)
                )

    return []
