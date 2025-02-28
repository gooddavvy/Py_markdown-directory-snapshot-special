import os
import sys
import time
import streamlit as st

# Add parent directory to Python path for imports if not already added
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from snapshot_generator import generate_markdown_snapshot
from token_counter import count_tokens

# --- Global variable to track checkbox keys ---
checkbox_keys = []

# --- Global Defaults ---
DEFAULT_IGNORED_NAMES = {".git", "node_modules", "__pycache__", "venv", "dist", "build"}
INDENT_MULTIPLIER = 2


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

def display_directory_tree(root_path, indent=0, sort_files=True, parent_checked=True):
    """
    Recursively displays a directory tree with checkboxes in the sidebar.
    Each folder is rendered with a toggleable arrow (► when collapsed, ▼ when expanded)
    so that its contents can be hidden or shown.
    
    Args:
        root_path: The path to display
        indent: Current indentation level
        sort_files: Whether to sort entries alphabetically
        parent_checked: Whether the parent folder is checked
    
    Returns a list of absolute paths that are unchecked.
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
        is_folder = os.path.isdir(full_path)

        # Create an expand key for folders so we know if they're expanded or collapsed
        if is_folder:
            expand_key = f"expand_{full_path}"
            if expand_key not in st.session_state:
                st.session_state[expand_key] = True  # default: expanded
            arrow = "▼" if st.session_state[expand_key] else "►"
        else:
            arrow = ""  # No arrow for files

        # We'll produce either 2 or 3 columns:
        # - If indent > 0, the first column is our "spacer".
        # - The second column is for the arrow or an empty string (for files).
        # - The third column is the checkbox for the file/folder name.
        if indent > 0:
            # Indent must be positive, so we create a "spacer" column, arrow column, and checkbox column
            spacer_col, arrow_col, check_col = st.sidebar.columns([indent * 0.3, 0.15, 0.85])
        else:
            # If indent == 0, we just have arrow and checkbox columns (no need for spacer)
            arrow_col, check_col = st.sidebar.columns([0.15, 0.85])

        # 1) Arrow Button Column
        if indent > 0:
            with arrow_col:
                if arrow:
                    # Click toggles expansion state
                    if st.button(arrow, key=f"toggle_{full_path}"):
                        st.session_state[expand_key] = not st.session_state[expand_key]
        else:
            # indent=0, so we only have arrow_col and check_col
            with arrow_col:
                if arrow:
                    if st.button(arrow, key=f"toggle_{full_path}"):
                        st.session_state[expand_key] = not st.session_state[expand_key]

        # 2) Checkbox Column
        if indent > 0:
            with check_col:
                default_value = False if entry in DEFAULT_IGNORED_NAMES else True
                if parent_checked:
                    item_checked = st.checkbox(
                        f"{entry}/" if is_folder else f"{entry}",
                        value=default_value,
                        key=full_path
                    )
                else:
                    # Parent is unchecked, so disable
                    st.checkbox(
                        f"{entry}/" if is_folder else f"{entry}",
                        value=False,
                        key=full_path,
                        disabled=True
                    )
                    item_checked = False
        else:
            with check_col:
                default_value = False if entry in DEFAULT_IGNORED_NAMES else True
                if parent_checked:
                    item_checked = st.checkbox(
                        f"{entry}/" if is_folder else f"{entry}",
                        value=default_value,
                        key=full_path
                    )
                else:
                    st.checkbox(f"{entry}/" if is_folder else f"{entry}",
                                value=False, key=full_path, disabled=True)
                    item_checked = False

        # Record this path in ignored_paths if it was unchecked
        if not item_checked:
            ignored_paths.append(os.path.abspath(full_path))

        # If it's a folder and expanded, recurse:
        if is_folder and arrow and st.session_state[expand_key]:
            child_ignored = display_directory_tree(
                full_path,
                indent=indent + 1,
                sort_files=sort_files,
                parent_checked=item_checked
            )
            ignored_paths.extend(child_ignored)

    return ignored_paths

def get_manual_ignore_list(folder_path):
    """
    Returns a list of additional ignore patterns entered manually by the user.
    If a pattern is not an absolute path, it is assumed to be relative to folder_path.
    """
    manual_input = st.sidebar.text_area("Manual Ignore Patterns (*optional*, one per line)", height=100)
    manual_patterns = [line.strip() for line in manual_input.splitlines() if line.strip()]
    ignore_list = []
    for pattern in manual_patterns:
        if os.path.isabs(pattern):
            ignore_list.append(os.path.abspath(pattern))
        else:
            ignore_list.append(os.path.abspath(os.path.join(folder_path, pattern)))
    return ignore_list

# --- Sidebar Controls ---

st.sidebar.markdown("Directory Snapshot Tool <span class='beta-badge'>BETA</span>", unsafe_allow_html=True)

# "Select Folder" area: Because a native folder picker isn't available in Streamlit,
# the user enters a folder path manually.
folder_path = st.sidebar.text_input("Enter your absolute directory path", value="", placeholder="e.g., /home/user/my_project")


# Clear and refresh buttons for the sidebar selections.
if st.sidebar.button("🗑️ Clear Selections"):
    clear_checkbox_states()

if st.sidebar.button("🔄 Refresh Tree"):
    clear_checkbox_states()

sort_files = st.sidebar.checkbox("Sort files A-Z", value=True)

if folder_path and os.path.isdir(folder_path):
    st.sidebar.markdown("## Directory Tree")
    tree_ignored = display_directory_tree(folder_path, indent=0, sort_files=sort_files, parent_checked=True)
    manual_ignored = get_manual_ignore_list(folder_path)
    final_ignore_list = list(set(tree_ignored + manual_ignored))
else:
    st.sidebar.info("Please enter a valid absolute directory path above.")

# --- Main Content Area ---
st.markdown("# Directory Snapshot Tool <span class='beta-badge'>BETA</span>", unsafe_allow_html=True)
st.markdown("""
This tool creates a markdown snapshot of your directory.
Files and folders that are unchecked in the sidebar will be ignored.
When you are ready, click the **Generate Snapshot** button below!
""")

# Add text area for side notes
side_text = st.text_area("Add notes to append to the snapshot (*optional*)", height=100, help="This text will appear at the end of your snapshot")

if st.button("Generate Snapshot"):
    if not folder_path or not os.path.isdir(folder_path):
        st.error("Please provide a valid folder path before generating a snapshot.")
    else:
        with st.spinner("Generating snapshot..."):
            try:
                # Generate the basic snapshot
                generate_markdown_snapshot(folder_path, final_ignore_list)
                
                # Append the side text if provided
                if side_text:
                    with open("output.md", "a", encoding="utf-8") as f:
                        f.write("\n\n==========================================================\n\n")
                        f.write(side_text)
                
                time.sleep(0.5)
                st.success("Snapshot created successfully!")
                try:
                    with open("output.md", "r", encoding="utf-8") as f:
                        snapshot_content = f.read()
                    st.markdown(f"> The following snapshot contains {count_tokens(snapshot_content)} AI natural language tokens \n#### Snapshot (output.md):")
                    st.code(snapshot_content, language="txt")
                except Exception as e:
                    st.error(f"Snapshot was generated but there was an error reading 'output.md': {e}")
            except Exception as e:
                st.error(f"Error generating snapshot: {e}")

with st.expander("About / Instructions"):
    st.markdown("""
    **Usage Instructions:**

    1. **Select Directory:**  
       Enter the absolute path of the directory you want to snapshot.


    2. **Directory Tree:**  
       Use the checkboxes in the sidebar to select which files and folders to include.  
       *Unchecked items will be ignored in the snapshot.*  
       The default ignored items are: `.git`, `node_modules`, `__pycache__`, `venv`, `dist`, `build`.

    3. **Manual Ignore Patterns (*optional*):**  
       Enter additional ignore patterns (one per line). Non‐absolute patterns will be treated as relative to the selected folder.

    4. **Generate Snapshot:**  
       Click the **Generate Snapshot** button to create an `output.md` file containing your snapshot.

    **Note:**  
    If you encounter any issues (e.g. permissions or file access errors), please check that the folder path is correct and that you have read access to the files.
    """)

st.markdown("© 2025 Py_markdown-directory-snapshot-special")