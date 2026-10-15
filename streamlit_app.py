
import heapq

import plotly.graph_objects as go
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="NEXUS | Autonomous Navigation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROWS = 12
COLS = 15
START = (1, 1)
GOAL = (10, 13)

DEFAULT_OBSTACLES = {
    (2, 3), (3, 3), (4, 3), (5, 3), (6, 3),
    (6, 5), (6, 6), (6, 7),
    (3, 8), (4, 8), (5, 8),
    (7, 10), (8, 10), (9, 10),
    (2, 12), (3, 12), (4, 12),
}


# =========================================================
# STYLING
# =========================================================
st.markdown(
    """
    <style>
    @import url(
      'https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap'
    );

    .stApp {
        background:
          radial-gradient(ellipse at 52% -10%, #172b43 0%, transparent 48%),
          #080d17;
        color: #eef4ff;
        font-family: 'Manrope', sans-serif;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        background: #0b1220;
        border-right: 1px solid #26364c;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1600px;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 4px 0 20px;
    }

    .brand-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 45px;
        height: 45px;
        background: linear-gradient(135deg, #1c3948, #15313b);
        border: 1px solid #32746f;
        border-radius: 13px;
        color: #48e0d0;
        font-size: 23px;
    }

    .brand-name {
        color: #f2f7ff;
        font-size: 18px;
        font-weight: 800;
        letter-spacing: -.6px;
    }

    .brand-sub {
        color: #8294ad;
        font-family: 'DM Mono', monospace;
        font-size: 10px;
        letter-spacing: 1.6px;
        margin-top: 3px;
    }

    .eyebrow {
        color: #48e0d0;
        font-family: 'DM Mono', monospace;
        font-size: 10px;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 9px;
    }

    .page-title {
        font-size: clamp(27px, 3vw, 39px);
        line-height: 1.18;
        font-weight: 800;
        letter-spacing: -1.5px;
        color: #f4f7ff;
        margin-bottom: 9px;
    }

    .page-subtitle {
        color: #93a5be;
        font-size: 13px;
        line-height: 1.8;
    }

    .header-status {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 9px 12px;
        border: 1px solid #2b4b4b;
        border-radius: 30px;
        color: #a8eee3;
        background: #102522;
        font-family: 'DM Mono', monospace;
        font-size: 10px;
        letter-spacing: .7px;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        background: #48e0d0;
        border-radius: 50%;
        display: inline-block;
    }

    .metric-card {
        background: linear-gradient(145deg, #131f31, #0e1725);
        border: 1px solid #293950;
        border-radius: 13px;
        padding: 17px 18px;
        min-height: 105px;
    }

    .metric-label {
        font-family: 'DM Mono', monospace;
        font-size: 9px;
        letter-spacing: 1.1px;
        color: #8196b1;
    }

    .metric-value {
        color: #f2f7ff;
        font-size: 25px;
        font-weight: 800;
        letter-spacing: -.8px;
        margin-top: 9px;
    }

    .metric-foot {
        color: #91a6c3;
        font-size: 10px;
        margin-top: 3px;
    }

    .panel-heading {
        font-size: 14px;
        font-weight: 800;
        color: #eff5ff;
    }

    .panel-caption {
        font-size: 11px;
        color: #8294ad;
        margin-top: 5px;
        line-height: 1.7;
    }

    .telemetry-label {
        color: #8093ac;
        font-family: 'DM Mono', monospace;
        font-size: 9px;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }

    .telemetry-value {
        color: #e9f1ff;
        font-size: 14px;
        font-weight: 700;
    }

    .legend-row {
        display: flex;
        flex-wrap: wrap;
        gap: 13px;
        margin: 15px 0 5px;
        color: #9aabc1;
        font-size: 10px;
    }

    .legend-item {
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .legend-swatch {
        width: 9px;
        height: 9px;
        display: inline-block;
        border-radius: 3px;
    }

    .stButton > button {
        border-radius: 9px;
        min-height: 42px;
        font-weight: 700;
        font-size: 12px;
        border: 1px solid #30435d;
        transition: all .15s ease;
    }

    .stButton > button[kind="primary"] {
        color: #07151a;
        background: linear-gradient(100deg, #50e2d2, #63c9ff);
        border: none;
    }

    .stButton > button:hover {
        border-color: #48e0d0;
    }

    div[data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg, #45cfc3, #548bff);
    }

    hr {
        border-color: #27374b;
    }

    .footer-note {
        color: #71849e;
        font-size: 10px;
        line-height: 1.8;
        border-top: 1px solid #243247;
        padding-top: 15px;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# A* PATH PLANNING
# =========================================================
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(start, goal, obstacles):
    """Find a shortest four-directional path using A*."""
    if start in obstacles or goal in obstacles:
        return []

    frontier = [(heuristic(start, goal), 0, start)]
    came_from = {}
    costs = {start: 0}
    visited = set()

    while frontier:
        _, current_cost, current = heapq.heappop(frontier)

        if current in visited:
            continue

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return list(reversed(path))

        visited.add(current)
        row, col = current

        neighbors = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]

        for neighbor in neighbors:
            nr, nc = neighbor

            if not (0 <= nr < ROWS and 0 <= nc < COLS):
                continue
            if neighbor in obstacles or neighbor in visited:
                continue

            new_cost = current_cost + 1

            if new_cost < costs.get(neighbor, float("inf")):
                costs[neighbor] = new_cost
                came_from[neighbor] = current
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(
                    frontier, (priority, new_cost, neighbor)
                )

    return []


# =========================================================
# SESSION STATE
# =========================================================
if "obstacles" not in st.session_state:
    st.session_state.obstacles = set(DEFAULT_OBSTACLES)

if "robot_index" not in st.session_state:
    st.session_state.robot_index = 0


def reset_robot():
    st.session_state.robot_index = 0


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown(
        """
        <div class="brand">
          <div class="brand-icon">⌘</div>
          <div>
            <div class="brand-name">NEXUS<span style="color:#48e0d0">.AI</span></div>
            <div class="brand-sub">AUTONOMOUS SYSTEMS LAB</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("#### ENVIRONMENT")

    mode = st.radio(
        "Obstacle configuration",
        ["Standard map", "Custom map"],
        label_visibility="collapsed",
        key="map_mode",
    )

    if mode == "Standard map":
        st.session_state.obstacles = set(DEFAULT_OBSTACLES)
        st.caption("12 × 15 grid · predefined obstacles")
    else:
        st.caption("Choose a grid cell to add or remove an obstacle.")

        edit_row = st.number_input(
            "Grid row",
            min_value=0,
            max_value=ROWS - 1,
            value=6,
            key="edit_row",
        )
        edit_col = st.number_input(
            "Grid column",
            min_value=0,
            max_value=COLS - 1,
            value=4,
            key="edit_col",
        )

        if st.button("＋ Toggle obstacle", use_container_width=True):
            cell = (int(edit_row), int(edit_col))

            if cell in (START, GOAL):
                st.warning("Start and goal cells cannot be blocked.")
            elif cell in st.session_state.obstacles:
                st.session_state.obstacles.remove(cell)
                reset_robot()
                st.rerun()
            else:
                st.session_state.obstacles.add(cell)
                reset_robot()
                st.rerun()

        if st.button("Restore standard map", use_container_width=True):
            st.session_state.obstacles = set(DEFAULT_OBSTACLES)
            reset_robot()
            st.rerun()

    st.markdown("---")
    st.markdown("#### NAVIGATION CONTROLS")
    st.caption("Planner: A* · Heuristic: Manhattan distance")

    if st.button("↺ Reset robot", use_container_width=True):
        reset_robot()
        st.rerun()

    st.markdown("---")
    st.markdown("#### SYSTEM INFORMATION")

    st.markdown(
        """
        <div class="telemetry-label">PLANNING ENGINE</div>
        <div class="telemetry-value">A* Search</div>
        <br/>
        <div class="telemetry-label">MOVEMENT MODEL</div>
        <div class="telemetry-value">4-directional grid</div>
        <br/>
        <div class="telemetry-label">PERCEPTION SOURCE</div>
        <div class="telemetry-value">Simulated obstacles</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="footer-note">
        WEB SIMULATOR · SOFTWARE PROTOTYPE<br/>
        Camera detections are not connected to this planner.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# COMPUTE ROUTE AND POSITION
# =========================================================
obstacles = set(st.session_state.obstacles)
path = astar(START, GOAL, obstacles)

if not path:
    st.session_state.robot_index = 0
    robot = START
else:
    st.session_state.robot_index = min(
        st.session_state.robot_index, len(path) - 1
    )
    robot = path[st.session_state.robot_index]

total_moves = max(len(path) - 1, 0)
moves_completed = st.session_state.robot_index
progress = moves_completed / total_moves if total_moves else 0.0

if not path:
    status = "NO ROUTE"
elif robot == GOAL:
    status = "ARRIVED"
elif moves_completed:
    status = "IN MOTION"
else:
    status = "READY"


# =========================================================
# HEADER
# =========================================================
header_left, header_right = st.columns([4, 1.2])

with header_left:
    st.markdown(
        """
        <div class="eyebrow">ROBOTICS / SIMULATION / 001</div>
        <div class="page-title">Autonomous Navigation</div>
        <div class="page-subtitle">
        Path planning and obstacle avoidance in an interactive
        virtual environment.
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_right:
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="text-align:right">
          <div class="header-status">
            <span class="status-dot"></span>{status}
          </div>
          <div style="color:#7488a3;font-size:10px;margin-top:10px">
            SIMULATION ENGINE ONLINE
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br/>", unsafe_allow_html=True)


# =========================================================
# METRIC CARDS
# =========================================================
metric_columns = st.columns(4)

metric_data = [
    ("GRID DIMENSIONS", f"{ROWS} × {COLS}", "180 total cells"),
    ("ACTIVE OBSTACLES", str(len(obstacles)), "Blocked cells"),
    ("SHORTEST ROUTE", str(total_moves) if path else "—", "Required moves"),
    (
        "ROBOT PROGRESS",
        f"{progress * 100:.0f}%",
        f"{moves_completed} of {total_moves} moves",
    ),
]

for col, (label, value, foot) in zip(metric_columns, metric_data):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
              <div class="metric-label">{label}</div>
              <div class="metric-value">{value}</div>
              <div class="metric-foot">{foot}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br/>", unsafe_allow_html=True)


# =========================================================
# SIMULATION VIEWPORT
# =========================================================
sim_col, control_col = st.columns([1.8, 1], gap="large")

with sim_col:
    st.markdown(
        """
        <div class="panel-heading">Live simulation viewport</div>
        <div class="panel-caption">
        Grid-based world model · The highlighted route is recalculated
        when the obstacle map changes.
        </div>
        """,
        unsafe_allow_html=True,
    )

    z = []
    labels = []
    path_set = set(path)

    for row in range(ROWS):
        z_row = []
        label_row = []

        for col in range(COLS):
            cell = (row, col)

            if cell == robot:
                z_row.append(5)
                label_row.append("R")
            elif cell == START:
                z_row.append(4)
                label_row.append("S")
            elif cell == GOAL:
                z_row.append(3)
                label_row.append("G")
            elif cell in obstacles:
                z_row.append(2)
                label_row.append("■")
            elif cell in path_set:
                z_row.append(1)
                label_row.append("")
            else:
                z_row.append(0)
                label_row.append("")

        z.append(z_row)
        labels.append(label_row)

    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            text=labels,
            texttemplate="%{text}",
            zmin=0,
            zmax=5,
            showscale=False,
            xgap=4,
            ygap=4,
            colorscale=[
                [0.00, "#111d2e"],
                [0.19, "#111d2e"],
                [0.20, "#236b87"],
                [0.39, "#236b87"],
                [0.40, "#303d51"],
                [0.59, "#303d51"],
                [0.60, "#e05b68"],
                [0.79, "#e05b68"],
                [0.80, "#287d69"],
                [0.99, "#287d69"],
                [1.00, "#f4c95d"],
            ],
            hovertemplate="Column %{x} · Row %{y}<extra></extra>",
        )
    )

    # Explicit tick values and bounds prevent incorrect automatic labels.
    fig.update_layout(
        height=530,
        margin=dict(l=8, r=8, t=28, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#9aadc6", size=10),
        xaxis=dict(
            title="COLUMN",
            tickmode="array",
            tickvals=list(range(COLS)),
            ticktext=[str(c) for c in range(COLS)],
            side="top",
            range=[-0.5, COLS - 0.5],
            fixedrange=True,
        ),
        yaxis=dict(
            title="ROW",
            tickmode="array",
            tickvals=list(range(ROWS)),
            ticktext=[str(r) for r in range(ROWS)],
            range=[ROWS - 0.5, -0.5],
            scaleanchor="x",
            scaleratio=1,
            fixedrange=True,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False, "scrollZoom": False},
    )

    st.markdown(
        """
        <div class="legend-row">
          <span class="legend-item"><i class="legend-swatch" style="background:#287d69"></i>START</span>
          <span class="legend-item"><i class="legend-swatch" style="background:#e05b68"></i>GOAL</span>
          <span class="legend-item"><i class="legend-swatch" style="background:#303d51"></i>OBSTACLE</span>
          <span class="legend-item"><i class="legend-swatch" style="background:#236b87"></i>PLANNED ROUTE</span>
          <span class="legend-item"><i class="legend-swatch" style="background:#f4c95d"></i>ROBOT</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# ROBOT CONTROL PANEL
# =========================================================
with control_col:
    st.markdown(
        """
        <div class="panel-heading">Robot control center</div>
        <div class="panel-caption">
        Navigate the robot through the computed shortest path.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br/>", unsafe_allow_html=True)

    if not path:
        st.error("No valid route exists. Change the obstacle layout.")
    elif robot == GOAL:
        st.success("Destination reached successfully.")
    else:
        st.info("Robot is ready for navigation.")

    st.progress(progress)

    st.markdown(
        f"""
        <div class="metric-card">
          <div class="telemetry-label">CURRENT COORDINATES</div>
          <div class="telemetry-value">
            ROW {robot[0]} / COLUMN {robot[1]}
          </div>
          <hr style="border-color:#293950;margin:16px 0"/>
          <div class="telemetry-label">MOVES COMPLETED</div>
          <div class="telemetry-value">{moves_completed} / {total_moves}</div>
          <hr style="border-color:#293950;margin:16px 0"/>
          <div class="telemetry-label">DESTINATION</div>
          <div class="telemetry-value">
            ROW {GOAL[0]} / COLUMN {GOAL[1]}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br/>", unsafe_allow_html=True)

    if st.button(
        "▶ Move one step",
        type="primary",
        use_container_width=True,
        disabled=(not path or robot == GOAL),
    ):
        st.session_state.robot_index += 1
        st.rerun()

    if st.button(
        "⏩ Complete navigation",
        use_container_width=True,
        disabled=(not path or robot == GOAL),
    ):
        st.session_state.robot_index = len(path) - 1
        st.rerun()

    if st.button("↺ Reset to start", use_container_width=True):
        reset_robot()
        st.rerun()

    st.markdown("<br/>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="panel-heading">Planner diagnostics</div>
        <div class="panel-caption">
        Algorithm: A* search<br/>
        Heuristic: Manhattan distance<br/>
        Motion: Four-directional<br/>
        Obstacles: Static simulated grid
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
    <div class="footer-note">
    NEXUS.AI · AUTONOMOUS NAVIGATION PROTOTYPE<br/>
    This browser application simulates a grid environment. Webcam and
    YOLO object detection are separate modules and do not currently
    control the navigation route.
    </div>
    """,
    unsafe_allow_html=True,
)
