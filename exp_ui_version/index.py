import streamlit as st
import sys
import os

# Add parent directory to Python path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# --- Configuration & CSS for Dark Theme ---
st.set_page_config(
    page_title="Directory Tools",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📸"
)

st.markdown("""
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
    /* BETA badge styling */
    .beta-badge {
        background: linear-gradient(45deg, #4b6eff, #ff4b4b);
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.8em;
        margin-left: 8px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

from ui_utils import navbar_html  # Import the shared navbar
st.markdown(navbar_html, unsafe_allow_html=True)  # Display the navbar

st.title("Directory Tools")
st.markdown("""
Welcome to Directory Tools! This application helps you:
- 📸 Generate directory snapshots in markdown format
- 📑 Recreate directory structures from snapshots

Use the navigation bar above to access these features.
""")

# URL-based navigation
current_page = st.query_params.get("nav", "snapshot")

# Import and run the appropriate page
if current_page == "recreation":
    import recreation_tab
else:
    import snapshot_tab

# Footer
st.markdown("© 2025 Py_markdown-directory-snapshot-special")