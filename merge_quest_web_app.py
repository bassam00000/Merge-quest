import streamlit as st
import random

st.set_page_config(page_title="Merge Quest Web", layout="centered")

ROWS, COLS = 5, 5
ELEMENTS = [1, 2, 3]
COLORS = {
    0: "#eeeeee",
    1: "#a1cfff",
    2: "#91f2a1",
    3: "#f3a1a1",
    4: "#f5e15e",
    5: "#c38fff"
}

# تهيئة الشبكة في الجلسة
if "grid" not in st.session_state:
    st.session_state.grid = [[random.choice(ELEMENTS) for _ in range(COLS)] for _ in range(ROWS)]
    st.session_state.score = 0
    st.session_state.goal = 100
    st.session_state.selected = None

def render_grid():
    for i in range(ROWS):
        cols = st.columns(COLS)
        for j in range(COLS):
            val = st.session_state.grid[i][j]
            label = f"{val}" if val > 0 else ""
            button = cols[j].button(label, key=f"{i}-{j}", help="Click to select", 
                                    args=(i, j,))
            cols[j].markdown(
                f"<div style='height: 60px; background-color: {COLORS.get(val, '#ffffff')};"
                f" display: flex; align-items: center; justify-content: center; font-weight: bold;'>"
                f"{label}</div>", unsafe_allow_html=True)
            if button:
                handle_click(i, j)

def handle_click(i, j):
    if st.session_state.selected is None:
        st.session_state.selected = (i, j)
    else:
        r1, c1 = st.session_state.selected
        r2, c2 = i, j
        if abs(r1 - r2) + abs(c1 - c2) == 1:
            grid = st.session_state.grid
            grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]
            if not merge_elements():
                grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]
        st.session_state.selected = None

def merge_elements():
    merged = False
    grid = st.session_state.grid
    score = 0
    for i in range(ROWS):
        for j in range(COLS):
            val = grid[i][j]
            if val == 0:
                continue
            neighbors = []
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                ni, nj = i+dx, j+dy
                if 0 <= ni < ROWS and 0 <= nj < COLS and grid[ni][nj] == val:
                    neighbors.append((ni, nj))
            if len(neighbors) >= 2:
                grid[i][j] = min(val+1, 5)
                for ni, nj in neighbors:
                    grid[ni][nj] = 0
                st.session_state.score += 10 * val
                merged = True
    refill_grid()
    return merged

def refill_grid():
    for i in range(ROWS):
        for j in range(COLS):
            if st.session_state.grid[i][j] == 0:
                st.session_state.grid[i][j] = random.choice(ELEMENTS)

# واجهة المستخدم
st.title("Merge Quest (Web Version)")
st.markdown("Merge 3 similar tiles to upgrade and earn points!")

render_grid()

st.markdown(f"**Score:** {st.session_state.score} / {st.session_state.goal}")

if st.session_state.score >= st.session_state.goal:
    st.success("You Win!")

if st.button("Reset Game"):
    st.session_state.grid = [[random.choice(ELEMENTS) for _ in range(COLS)] for _ in range(ROWS)]
    st.session_state.score = 0
    st.session_state.selected = None
