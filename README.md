# AI-Based Autonomous Navigation System

An interactive AI navigation project that demonstrates autonomous path planning, obstacle avoidance, and visual navigation through a grid-based simulation.

**Live Demo:** https://ai-autonomous-navigation-system-kykamnkn9gqulibwoctvue.streamlit.app/

**GitHub Repository:** https://github.com/jatingujju/AI-Autonomous-Navigation-System

## Project Overview

This project explores how an autonomous navigation system can find a path from a starting point to a destination while avoiding obstacles. It combines path-planning algorithms, a simulation environment, and an interactive Streamlit dashboard.

## Key Features

- **A* Path Planning:** Finds a route between the start and goal while avoiding blocked grid cells.
- **Interactive Navigation:** Move through the planned route one step at a time or complete the navigation automatically.
- **Obstacle Management:** Explore navigation using obstacles and supported custom map configurations.
- **Visual Simulation:** View the grid, planned route, obstacles, start point, and destination.
- **Navigation Controls:** Start, advance, complete, and reset the simulation.
- **Computer Vision Components:** Separate camera-capture and YOLO-based object-detection modules for experimentation.

## Technology Stack

- Python
- A* Search Algorithm
- Pygame
- Streamlit
- Plotly
- NumPy
- OpenCV
- Ultralytics YOLO

## How It Works

1. Define the starting position and destination.
2. Represent the environment as a grid containing obstacles.
3. Use A* search to calculate a valid route.
4. Visualize the route and environment in the dashboard.
5. Simulate movement and monitor navigation progress.
6. Reset the simulation to explore another run.

## Run the Streamlit Dashboard Locally

Clone the repository:

```bash
git clone https://github.com/jatingujju/AI-Autonomous-Navigation-System.git
cd AI-Autonomous-Navigation-System
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install the dashboard dependencies:

```bash
pip install -r requirements.txt
```

Launch the dashboard:

```bash
python -m streamlit run streamlit_app.py
```

## Project Scope and Limitations

This project demonstrates navigation in a simulated environment. The camera and YOLO detection components are separate from the current A* route planner; detected objects do not automatically update the planned route. The project has not been validated on a physical robot.

## Future Improvements

- Integrate detected obstacles with real-time path replanning.
- Add dynamic obstacle movement to the simulation.
- Compare A* with algorithms such as Dijkstra's and BFS.
- Add navigation performance metrics and benchmarking.
- Explore deployment on a physical robot platform.

## Author

**Jatin Gujarathi**

GitHub: https://github.com/jatingujju

LinkedIn: https://www.linkedin.com/in/jatin-gujarathi-bb16a7221/

---

*Built as a hands-on project exploring AI, path planning, simulation, and computer vision.*
