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

def clear_checkbox_states():
    """
    Clears the session state for all checkboxes.
    This forces the checkboxes to revert to their default values.
    """
    global checkbox_keys
    for key in checkbox_keys:
        if key in st.session_state:
            del st.session_state[key]

def display_directory_tree(root_path, ignore_set, indent=0, sort_files=True):
    """
    Displays a collapsible, checkbox-enabled tree view of the directory at `root_path`.
    Returns a list of absolute paths that are unchecked (ignored).
    
    Parameters:
    -----------
    root_path: str or Path
        The folder path to display.
    ignore_set: set
        A set of absolute paths that have already been marked as ignored
        (either from a parent's checkbox or manually).
    indent: int
        Used to calculate indentation (number of 4-space increments).
    sort_files: bool
        Whether to sort folder entries A-Z.
    """

    # Convert to Path if needed
    root_path = Path(root_path)

    # If this folder is already ignored from a parent's checkbox, just return
    if str(root_path.resolve()) in ignore_set:
        return []

    ignored_paths = []

    try:
        entries = os.listdir(root_path)
        if sort_files:
            entries = sorted(entries)
    except Exception as e:
        st.sidebar.error(f"Error reading directory {root_path}: {e}")
        return []

    # We'll show the folder’s content inside an expander
    # But first we display a line with an overall folder checkbox + label
    indent_str = "&nbsp;" * 4 * indent  # Visual indentation in HTML
    folder_label = f"{indent_str}{root_path.name}/"

    # Create a unique key for the folder checkbox to avoid collisions
    folder_checkbox_key = str(root_path.resolve()) + "_folder_checkbox"
    checkbox_keys.append(folder_checkbox_key)

    # By default, let's assume folders are checked. You can adjust logic as needed.
    folder_checked = st.sidebar.checkbox(
        folder_label,
        value=True,
        key=folder_checkbox_key
    )

    if not folder_checked:
        # Mark this entire folder (and its subtree) as ignored
        ignored_paths.append(str(root_path.resolve()))
        return ignored_paths

    # If folder is checked, show an expander for its children
    # The label for the expander will have a small arrow. 
    with st.sidebar.expander(folder_label, expanded=False):
        # Iterate over items inside this folder
        for entry in entries:
            full_path = root_path / entry
            if full_path.is_dir():
                # Recursively display subfolder
                sub_ignored = display_directory_tree(
                    root_path=full_path,
                    ignore_set=ignore_set.union(ignored_paths),
                    indent=indent + 1,
                    sort_files=sort_files
                )
                ignored_paths.extend(sub_ignored)
            else:
                # It's a file; show it with a checkbox
                file_checkbox_key = str(full_path.resolve()) + "_file_checkbox"
                checkbox_keys.append(file_checkbox_key)

                file_indent_str = "&nbsp;" * 4 * (indent + 1)
                file_label = f"{file_indent_str}{entry}"
                file_checked = st.checkbox(
                    file_label,
                    value=True,
                    key=file_checkbox_key
                )
                if not file_checked:
                    ignored_paths.append(str(full_path.resolve()))

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

# "Select Folder" area
folder_path = st.sidebar.text_input("Enter the folder path", value="", placeholder="e.g., /home/user/my_project")

if st.sidebar.button("🗑️ Clear Selections"):
    clear_checkbox_states()

if st.sidebar.button("🔄 Refresh Tree"):
    clear_checkbox_states()

sort_files = st.sidebar.checkbox("Sort files A-Z", value=True)

if folder_path and os.path.isdir(folder_path):
    st.sidebar.markdown("### Directory Tree")
    tree_ignored = display_directory_tree(folder_path, sort_files=sort_files)
    manual_ignored = get_manual_ignore_list(folder_path)
    final_ignore_list = list(set(tree_ignored + manual_ignored))
else:
    st.sidebar.info("Please enter a valid folder path above.")

# --- Main Content Area ---
st.title("Directory Snapshot Tool")
st.markdown("""
This tool creates a markdown snapshot of your directory.
Files and folders that are unchecked in the sidebar will be ignored.
When you are ready, click the **Generate Snapshot** button below.
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
