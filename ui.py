import os
import time
import streamlit as st
from snapshot_generator import generate_markdown_snapshot

# --- Global variable to track checkbox keys ---
checkbox_keys = []

# --- Configuration & CSS for Dark Theme ---
st.set_page_config(
    page_title="Directory Snapshot Tool",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📸"
)

st.markdown(
    """
    <style>
    /* Main background */
    .reportview-container {
        background-color: #121212;
        color: #e0e0e0;
    }
    /* Sidebar background */
    .sidebar .sidebar-content {
        background-color: #1e1e1e;
    }
    /* Button styling */
    div.stButton > button {
        background-color: #1f6aa5;
        color: white;
        border: none;
        padding: 0.5em 1em;
        border-radius: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Global Defaults ---
DEFAULT_IGNORED_NAMES = {".git", "node_modules", "__pycache__", "venv", "dist", "build"}

# --- Helper Functions ---

def clear_checkbox_states():
    """
    Clears the session state for all checkboxes by deleting their keys.
    This forces the checkboxes to revert to their default values.
    """
    global checkbox_keys
    for key in checkbox_keys:
        if key in st.session_state:
            del st.session_state[key]

def display_directory_tree(root_path, indent=0, sort_files=True):
    """
    Recursively displays a directory tree with checkboxes in the sidebar.
    Each folder is rendered with a toggleable arrow (► when collapsed, ▼ when expanded)
    so that its contents can be hidden or shown.
    
    Returns a list of absolute paths that were unchecked.
    """
    global checkbox_keys
    ignored_paths = []
    try:
        entries = os.listdir(root_path)
        if sort_files:
            entries = sorted(entries)
    except Exception as e:
        st.sidebar.error(f"Error reading directory {root_path}: {e}")
        return []

    for entry in entries:
        full_path = os.path.join(root_path, entry)
        indent_px = indent * 20
        if os.path.isdir(full_path):
            # Set up a session state key to hold the expansion state for this folder
            expand_key = f"expand_{full_path}"
            if expand_key not in st.session_state:
                st.session_state[expand_key] = True  # default: expanded
            arrow = "▼" if st.session_state[expand_key] else "►"

            # Render the folder row inside a container that applies left margin
            with st.sidebar.container():
                st.markdown(f"<div style='margin-left: {indent_px}px'>", unsafe_allow_html=True)
                # Create two inline columns: one for the toggle arrow and one for the checkbox.
                cols = st.columns([0.2, 0.8])
                with cols[0]:
                    if st.button(arrow, key=f"toggle_{full_path}"):
                        st.session_state[expand_key] = not st.session_state[expand_key]
                with cols[1]:
                    default_value = False if entry in DEFAULT_IGNORED_NAMES else True
                    if not st.checkbox(f"{entry}/", value=default_value, key=full_path):
                        ignored_paths.append(os.path.abspath(full_path))
                st.markdown("</div>", unsafe_allow_html=True)
            # Only display the children if the folder is expanded.
            if st.session_state[expand_key]:
                child_ignored = display_directory_tree(full_path, indent=indent+1, sort_files=sort_files)
                ignored_paths.extend(child_ignored)
        else:
            # Render a file entry with its own left margin.
            checkbox_key = full_path
            checkbox_keys.append(checkbox_key)
            indent_px = indent * 20
            with st.sidebar.container():
                st.markdown(f"<div style='margin-left: {indent_px}px'>", unsafe_allow_html=True)
                if not st.checkbox(f"{entry}", value=True, key=checkbox_key):
                    ignored_paths.append(os.path.abspath(full_path))
                st.markdown("</div>", unsafe_allow_html=True)
    return ignored_paths

def get_manual_ignore_list(folder_path):
    """
    Returns a list of additional ignore patterns entered manually by the user.
    If a pattern is not an absolute path, it is assumed to be relative to folder_path.
    """
    manual_input = st.sidebar.text_area("Manual Ignore Patterns (one per line)", height=100)
    manual_patterns = [line.strip() for line in manual_input.splitlines() if line.strip()]
    ignore_list = []
    for pattern in manual_patterns:
        if os.path.isabs(pattern):
            ignore_list.append(os.path.abspath(pattern))
        else:
            ignore_list.append(os.path.abspath(os.path.join(folder_path, pattern)))
    return ignore_list

# --- Sidebar Controls ---

st.sidebar.title("Directory Snapshot Tool")

# "Select Folder" area: Because a native folder picker isn’t available in Streamlit,
# the user enters a folder path manually.
folder_path = st.sidebar.text_input("Enter the folder path", value="", placeholder="e.g., /home/user/my_project")

# Clear and refresh buttons for the sidebar selections.
if st.sidebar.button("🗑️ Clear Selections"):
    clear_checkbox_states()

if st.sidebar.button("🔄 Refresh Tree"):
    clear_checkbox_states()

sort_files = st.sidebar.checkbox("Sort files A-Z", value=True)

if folder_path and os.path.isdir(folder_path):
    st.sidebar.markdown("### Directory Tree")
    tree_ignored = display_directory_tree(folder_path, indent=0, sort_files=sort_files)
    manual_ignored = get_manual_ignore_list(folder_path)
    final_ignore_list = list(set(tree_ignored + manual_ignored))
else:
    st.sidebar.info("Please enter a valid folder path above.")

# --- Main Content Area ---
st.title("Directory Snapshot Tool")
st.markdown("""
This tool creates a markdown snapshot of your directory.
Files and folders that are unchecked in the sidebar will be ignored.
When you are ready, click the **Generate Snapshot** button below!
""")

if st.button("Generate Snapshot"):
    if not folder_path or not os.path.isdir(folder_path):
        st.error("Please provide a valid folder path before generating a snapshot.")
    else:
        with st.spinner("Generating snapshot..."):
            try:
                generate_markdown_snapshot(folder_path, final_ignore_list)
                time.sleep(0.5)
                st.success("Snapshot created successfully!")
                try:
                    with open("output.md", "r", encoding="utf-8") as f:
                        snapshot_content = f.read()
                    st.markdown("#### Snapshot (output.md):")
                    st.code(snapshot_content, language="markdown")
                except Exception as e:
                    st.error(f"Snapshot was generated but there was an error reading 'output.md': {e}")
            except Exception as e:
                st.error(f"Error generating snapshot: {e}")

with st.expander("About / Instructions"):
    st.markdown("""
    **Usage Instructions:**

    1. **Select Folder:**  
       Enter the absolute (or relative) path of the directory you want to snapshot.

    2. **Directory Tree:**  
       Use the checkboxes in the sidebar to select which files and folders to include.  
       *Unchecked items will be ignored in the snapshot.*  
       The default ignored items are: `.git`, `node_modules`, `__pycache__`, `venv`, `dist`, `build`.

    3. **Manual Ignore Patterns:**  
       Enter additional ignore patterns (one per line). Non‐absolute patterns will be treated as relative to the selected folder.

    4. **Generate Snapshot:**  
       Click the **Generate Snapshot** button to create an `output.md` file containing your snapshot.

    **Note:**  
    If you encounter any issues (e.g. permissions or file access errors), please check that the folder path is correct and that you have read access to the files.
    """)

st.markdown("© 2025 Py_markdown-directory-snapshot-special")
