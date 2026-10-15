
from src.path_planning import astar


def test_path_exists():
    start = (1, 1)
    goal = (3, 3)
    obstacles = {(1, 2), (2, 2)}

    path = astar(start, goal, obstacles, 5, 5)

    assert path, "A* failed to find a path."
    assert path[0] == start
    assert path[-1] == goal
    assert not any(cell in obstacles for cell in path)

    print("PASS: Path found around obstacles.")


def test_start_equals_goal():
    start = (2, 2)

    path = astar(start, start, set(), 5, 5)

    assert path == [start]

    print("PASS: Start equals goal.")


def test_no_path_exists():
    start = (1, 1)
    goal = (1, 3)

    # Block all four possible directions from the start
    obstacles = {
        (0, 1),
        (2, 1),
        (1, 0),
        (1, 2)
    }

    path = astar(start, goal, obstacles, 5, 5)

    assert path == [], "A* should not find a path."

    print("PASS: Unreachable destination handled correctly.")


def test_obstacle_at_start():
    start = (1, 1)
    goal = (3, 3)

    path = astar(start, goal, {start}, 5, 5)

    assert path == []

    print("PASS: Obstacle at start handled correctly.")


if __name__ == "__main__":
    test_path_exists()
    test_start_equals_goal()
    test_no_path_exists()
    test_obstacle_at_start()

    print("\nAll four tests passed.")
