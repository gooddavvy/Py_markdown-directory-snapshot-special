# import os
# import streamlit as st
# from outdir_generator import generate_outdir


# st.markdown("# Directory Recreation Tool <span class='beta-badge'>BETA</span>", unsafe_allow_html=True)
# st.markdown("""
# This tool recreates a directory structure from a markdown snapshot.
# Upload your snapshot file and specify the output directory to begin!
# """)

# # Sidebar content
# with sidebar:
#     st.markdown("## Recreation Settings")
#     output_dir = st.text_input(
#         "Enter output directory path",
#         value="",
#         placeholder="e.g., /home/user/recreated_project"
#     )

#     st.markdown("## Upload Snapshot")
#     uploaded_file = st.file_uploader("Upload snapshot file (input.md)", type="md")

#     if uploaded_file is not None:
#         st.success("✅ File uploaded successfully")
#         st.markdown("### File Preview")
#         content = uploaded_file.getvalue().decode("utf-8")
#         st.code(content[:200] + "..." if len(content) > 200 else content, language="markdown")

# # Main content area
# if uploaded_file is not None:
#     st.markdown("### Full Snapshot Preview:")
#     content = uploaded_file.getvalue().decode("utf-8")
#     st.code(content[:500] + "..." if len(content) > 500 else content, language="markdown")

#     if st.button("Recreate Directory"):
#         if not output_dir:
#             st.error("Please specify an output directory path.")
#         else:
#             try:
#                 # Save uploaded content to input.md
#                 with open("input.md", "w", encoding="utf-8") as f:
#                     f.write(content)
                
#                 # Generate the directory structure
#                 with st.spinner("Recreating directory structure..."):
#                     generate_outdir(output_dir)
#                     st.success(f"Directory structure recreated successfully at: {output_dir}")
#             except Exception as e:
#                 st.error(f"Error recreating directory: {e}")
#             finally:
#                 # Clean up the temporary input.md file
#                 if os.path.exists("input.md"):
#                     os.remove("input.md")
# else:
#     st.info("Please upload a snapshot file (input.md) to begin.")

# with st.expander("About / Instructions"):
#     st.markdown("""
#     **Usage Instructions:**

#     1. **Upload Snapshot:**  
#         Use the sidebar to upload your snapshot file (input.md).

#     2. **Set Output Directory:**  
#         Specify where you want the recreated directory structure to be created.

#     3. **Review & Create:**  
#         Review the snapshot preview and click "Recreate Directory" when ready.

#     **Note:**  
#     The tool expects a properly formatted snapshot file. Make sure your input.md follows the correct format:
#     ```
#     ---FILESTART: path/to/file.ext---
#     File contents here
#     ---FILEEND---
#     ```
#     """) 








# -------------------------------------------------------------



















import streamlit as st

st.title("📑 Page 2")
st.write("Welcome to Page 2!")
