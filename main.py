import time
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb, to_hex

from algorithms.bubble_sort import bubble_sort
from algorithms.insertion_sort import insertion_sort
from algorithms.selection_sort import selection_sort
from algorithms.binary_search import binary_search


class AlgorithmVisualizer:
    def __init__(self, algorithms):
        self.algorithms = algorithms

    def get_algorithm(self, name):
        if name == "Binary Search":
            return binary_search
        return self.algorithms.get(name)


class FrameRenderer:
    @staticmethod
    def draw_state_fig(state, highlight=(), info="", bar_color="#4169E1", highlight_color="#FF7F0E"):
        plt.style.use('seaborn-v0_8-darkgrid')
        fig, ax = plt.subplots(figsize=(9, 4))
        if not isinstance(state, (list, tuple)) or (len(state) and isinstance(state[0], (list, tuple))):
            ax.text(0.5, 0.5, str(state), ha='center', va='center')
            ax.set_xticks([])
            ax.set_yticks([])
        else:
            n = len(state)
            base_rgb = to_rgb(bar_color)
            colors = [
                to_hex([
                    base_rgb[0] * (0.3 + 0.7 * (i / max(1, n - 1))),
                    base_rgb[1] * (0.3 + 0.7 * (i / max(1, n - 1))),
                    base_rgb[2] * (0.3 + 0.7 * (i / max(1, n - 1)))
                ]) for i in range(n)
            ]
            bars = ax.bar(range(n), state, color=colors, edgecolor='black')
            if highlight:
                for idx in (highlight if isinstance(highlight, (list, tuple)) else [highlight]):
                    if isinstance(idx, int) and 0 <= idx < len(bars):
                        bars[idx].set_color(highlight_color)
            ax.set_xlabel('Index')
            ax.set_ylabel('Value')
            ax.set_xticks(range(len(state)))
            ax.set_xlim(-0.5, max(len(state) - 0.5, 0.5))
            ax.set_ylim(0, max(state) * 1.1 if state else 1)
            for rect, val in zip(bars, state):
                height = rect.get_height()
                ax.annotate(f'{val}', xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=8)
        ax.set_title(info, fontsize=12)
        plt.tight_layout()
        return fig


ALGOS = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Selection Sort": selection_sort,
}

visualizer = AlgorithmVisualizer(ALGOS)
renderer = FrameRenderer()

st.set_page_config(page_title="Algorithm Visualizer", layout="wide")
st.title("Algorithm Visualizer — Web Demo")

with st.sidebar:
    st.header("Controls")
    algo_name = st.selectbox("Algorithm", list(ALGOS.keys()) + ["Binary Search"])
    st.markdown("**Array input (required)**")
    arr_text = st.text_input("Enter numbers separated by commas", "5,2,4,1,3")

    try:
        arr = [int(x.strip()) for x in arr_text.split(",") if x.strip() != '']
    except Exception:
        st.error("Invalid array - use comma separated integers")
        arr = []
    st.write(f"Array size: {len(arr)}")

    if algo_name == "Binary Search":
        target = st.number_input("Target value", value=arr[0] if arr else 0)

    # Color pickers for bar and highlight colors
    bar_color = st.color_picker("Choose bar color", "#4169E1")  # Default Royal Blue
    highlight_color = st.color_picker("Choose highlight color", "#FF7F0E")  # Default Orange

    base_delay_ms = 160
    if 'multiplier' not in st.session_state:
        st.session_state.multiplier = 2

    col_a, col_b, col_c = st.columns([1, 1, 2])
    with col_a:
        if st.button("Speed -"):
            st.session_state.multiplier = max(1, st.session_state.multiplier // 2)
    with col_b:
        if st.button("Speed +"):
            st.session_state.multiplier = st.session_state.multiplier * 4
    with col_c:
        st.write("Current multiplier:", f"{st.session_state.multiplier}x")

    preset_cols = st.columns([1, 1, 1, 1])
    presets = [1, 2, 4, 8]
    for pc, val in zip(preset_cols, presets):
        with pc:
            if st.button(f"{val}x"):
                st.session_state.multiplier = val
    multiplier = st.session_state.multiplier
    st.markdown("---")
    st.write("Playback")
    if 'playing' not in st.session_state:
        st.session_state.playing = False
    if 'frames' not in st.session_state:
        st.session_state.frames = []
    if 'idx' not in st.session_state:
        st.session_state.idx = 0

    if st.button("Generate frames"):
        if not arr:
            st.warning("Provide a valid array first.")
            st.session_state.frames = []
        else:
            algo_func = visualizer.get_algorithm(algo_name)
            if algo_name == "Binary Search":
                st.session_state.frames = list(algo_func(sorted(arr), int(target)))
            else:
                st.session_state.frames = list(algo_func(arr))
        st.session_state.idx = 0
        st.session_state.playing = False

    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("Play ▶"):
            st.session_state.playing = True
    with c2:
        if st.button("Pause ⏸"):
            st.session_state.playing = False
    with c3:
        if st.button("Step ⏭"):
            st.session_state.playing = False
            st.session_state.idx = min(st.session_state.idx + 1, max(len(st.session_state.frames) - 1, 0))

    if st.button("Reset"):
        st.session_state.idx = 0
        st.session_state.playing = False

    # Visual progress bar reflecting current frame
    total_frames = max(len(st.session_state.frames), 1)
    progress_val = st.session_state.idx / total_frames
    st.progress(progress_val)

placeholder = st.empty()

def render_frame_at(i: int):
    if 0 <= i < len(st.session_state.frames):
        frame = st.session_state.frames[i]
        fig = renderer.draw_state_fig(
            frame.get('state', []),
            frame.get('highlight', ()),
            frame.get('info', ''),
            bar_color=bar_color,
            highlight_color=highlight_color
        )
        placeholder.pyplot(fig)
        plt.close(fig)

if st.session_state.frames:
    render_frame_at(st.session_state.idx)

if st.session_state.playing and st.session_state.frames:
    delay = max(0.001, (base_delay_ms / max(1, multiplier)) / 1000.0)
    for i in range(st.session_state.idx, len(st.session_state.frames)):
        if not st.session_state.playing:
            break
        render_frame_at(i)
        st.session_state.idx = i + 1
        time.sleep(delay)
    st.session_state.playing = False
    if st.session_state.idx >= len(st.session_state.frames):
        st.success("Done")
