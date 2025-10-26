import time
import random
import streamlit as st
import matplotlib.pyplot as plt

from algorithms.bubble_sort import bubble_sort
from algorithms.insertion_sort import insertion_sort
from algorithms.selection_sort import selection_sort
from algorithms.binary_search import binary_search
from algorithms.merge_sort import merge_sort


ALGOS = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Selection Sort": selection_sort,
    "Merge Sort": merge_sort,
}


def draw_state_fig(state, highlight=(), info="", bar_color="#4C78A8", highlight_color="#EE994F"):
    """Draws a bar chart with axis labels, title, and highlight indices."""
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(9, 4))
    if not isinstance(state, (list, tuple)) or (len(state) and isinstance(state[0], (list, tuple))):
        ax.text(0.5, 0.5, str(state), ha='center', va='center')
        ax.set_xticks([])
        ax.set_yticks([])
    else:
        bars = ax.bar(range(len(state)), state, color=bar_color, edgecolor='black')
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
                        xytext=(0, 3), textcoords='offset points',
                        ha='center', va='bottom', fontsize=8)
    ax.set_title(info, fontsize=12)
    plt.tight_layout()
    return fig


st.set_page_config(page_title="Algorithm Visualizer", layout="wide")
st.title("Algorithm Visualizer — Web Demo")

# Sidebar controls
with st.sidebar:
    st.header("Controls")
    st.subheader("Configuration")
    with st.form("visualization_form"):
        algo_name = st.selectbox(
            "🔧 Select Algorithm",
            list(ALGOS.keys()) + ["Binary Search"],
            help="Choose the algorithm you want to visualize"
        )

        st.markdown("**📝 Array Input**")
        arr_text = st.text_input(
            "Enter numbers separated by commas",
            value="5,2,4,1,3",
            placeholder="e.g., 5,2,4,1,3",
            help="Enter integers separated by commas"
        )

        target = None
        if algo_name == "Binary Search":
            target = st.number_input("🎯 Target value to search for", value=5)

        submitted = st.form_submit_button("🚀 Generate Visualization", use_container_width=True)

        if submitted:
            try:
                arr = [int(x.strip()) for x in arr_text.split(",") if x.strip() != '']
                if not arr:
                    st.error("❌ Please enter at least one number")
                elif len(arr) > 50:
                    st.error("❌ Array too large! Please use 50 or fewer elements")
                else:
                    with st.spinner(f"Generating {algo_name} visualization..."):
                        if algo_name == "Binary Search":
                            sorted_arr = sorted(arr)
                            st.info(f"🔄 Array sorted for binary search: {sorted_arr}")
                            st.session_state.frames = list(binary_search(sorted_arr, int(target)))
                        else:
                            st.session_state.frames = list(ALGOS[algo_name](arr.copy()))
                        st.session_state.idx = 0
                        st.session_state.playing = False
                        st.success(f"✅ Generated {len(st.session_state.frames)} animation frames!")
            except ValueError:
                st.error("❌ Invalid input! Please enter only integers separated by commas")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

    try:
        arr = [int(x.strip()) for x in arr_text.split(",") if x.strip() != '']
        if arr:
            st.info(f"📊 Array size: **{len(arr)}**")
            st.write(f"Array preview: `{arr}`")
        else:
            st.warning("⚠️ Array is empty")
    except Exception:
        st.error("❌ Invalid array format - use comma separated integers")
        arr = []

    st.subheader("Playback Speed")
    base_delay_ms = 500
    if 'multiplier' not in st.session_state:
        st.session_state.multiplier = 1

    speed_cols = st.columns([1, 1])
    with speed_cols[0]:
        if st.button("🐌 Slower"):
            st.session_state.multiplier = max(0.25, st.session_state.multiplier / 2)
    with speed_cols[1]:
        if st.button("🚀 Faster"):
            st.session_state.multiplier = min(16, st.session_state.multiplier * 2)
    st.write(f"**Speed:** {st.session_state.multiplier}x")

    st.write("**Quick Presets:**")
    preset_cols = st.columns(4)
    presets = [0.5, 1, 2, 4]
    for i, (col, speed_val) in enumerate(zip(preset_cols, presets)):
        with col:
            if st.button(f"{speed_val}x", key=f"preset_{i}"):
                st.session_state.multiplier = speed_val
    st.markdown("---")

    if 'playing' not in st.session_state:
        st.session_state.playing = False
    if 'frames' not in st.session_state:
        st.session_state.frames = []
    if 'idx' not in st.session_state:
        st.session_state.idx = 0

    st.subheader("Colors")
    if "bar_color" not in st.session_state:
        st.session_state.bar_color = "#4C78A8"
    if "highlight_color" not in st.session_state:
        st.session_state.highlight_color = "#EE994F"

    st.session_state.bar_color = st.color_picker("Choose bar color", value=st.session_state.bar_color)
    st.session_state.highlight_color = st.color_picker("Choose highlight color", value=st.session_state.highlight_color)

    if st.session_state.frames:
        status = "🔴 Playing..." if st.session_state.playing else "⏸️ Paused"
        st.markdown(f"**Status:** {status}")

    control_cols = st.columns(4)
    with control_cols[0]:
        play_disabled = not st.session_state.frames or st.session_state.idx >= len(st.session_state.frames) - 1
        if st.button("▶️ Play", disabled=play_disabled):
            st.session_state.playing = True
    with control_cols[1]:
        if st.button("⏸️ Pause"):
            st.session_state.playing = False
    with control_cols[2]:
        step_disabled = not st.session_state.frames or st.session_state.idx >= len(st.session_state.frames) - 1
        if st.button("⏭️ Step", disabled=step_disabled):
            st.session_state.playing = False
            max_idx = max(len(st.session_state.frames) - 1, 0)
            st.session_state.idx = min(st.session_state.idx + 1, max_idx)
    with control_cols[3]:
        if st.button("🔄 Reset", disabled=not st.session_state.frames):
            st.session_state.idx = 0
            st.session_state.playing = False

    if not st.session_state.frames:
        st.info("🎬 Generate visualization frames to start animation")

# === Main visualization area ===
st.header("Visualization")

progress_container = st.container()
graph_container = st.container()


def update_progress_bar():
    if st.session_state.frames:
        total_frames = len(st.session_state.frames)
        current_frame = st.session_state.idx + 1
        progress_value = st.session_state.idx / max(total_frames - 1, 1)
        percentage = int(progress_value * 100)
        with progress_container:
            st.markdown(f"### 📊 Progress: {percentage}%")
            prog_col1, prog_col2 = st.columns([5, 1])
            with prog_col1:
                st.progress(progress_value)
            with prog_col2:
                st.metric("Frame", f"{current_frame}/{total_frames}")
            if 0 <= st.session_state.idx < len(st.session_state.frames):
                current_info = st.session_state.frames[st.session_state.idx].get('info', 'Algorithm Step')
                st.info(f"🔹 **Current Step:** {current_info}")
            st.markdown("---")


def render_frame_at(i: int):
    update_progress_bar()
    if st.session_state.frames and 0 <= i < len(st.session_state.frames):
        try:
            frame = st.session_state.frames[i]
            fig = draw_state_fig(
                frame.get('state', []),
                frame.get('highlight', ()),
                frame.get('info', 'Algorithm Step'),
                bar_color=st.session_state.get("bar_color", "#4C78A8"),
                highlight_color=st.session_state.get("highlight_color", "#EE994F"),
            )
            with graph_container:
                st.pyplot(fig)
            plt.close(fig)
        except Exception as e:
            with graph_container:
                st.error(f"Error rendering frame: {str(e)}")
    else:
        with progress_container:
            st.info("🎯 Select an algorithm and click 'Visualize!' to see the animation")


render_frame_at(st.session_state.idx)

# === Auto-play logic with celebration 🎉 ===
if st.session_state.playing and st.session_state.frames:
    delay = max(0.1, base_delay_ms / (1000.0 * st.session_state.multiplier))
    if st.session_state.idx < len(st.session_state.frames) - 1:
        time.sleep(delay)
        st.session_state.idx += 1
        st.rerun()
    else:
        # 🎉 Animation completed!
        st.session_state.playing = False
        st.session_state.idx = len(st.session_state.frames) - 1
        with st.sidebar:
            st.success("🎉 Animation Complete!")
        st.toast("✅ Array sorted successfully! 🎉")
        st.balloons()  # 🎈 Celebration effect here!
