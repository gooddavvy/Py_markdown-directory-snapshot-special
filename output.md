---FILESTART: input.md---
---FILESTART: hello_world.js---
console.log("This is from the author:")
console.log("Hello world!")
xx```xx
---FILEEND---

---FILESTART: ignore_this_file.txt---
Don't you dare look at my` contained contents!`
rt```rr
---FILEEND---

---FILESTART: accept_this_directory\ignore_this_thing.txt---
Don't you da`re look at my contained contents!
Ye`s, I'm a file```!
---FILEEND---

---FILESTART: accept_this_directory\greetings.txt---

```
Leoooo!!!! Wuzzupp!!!
```

---FILEEND---

---FILESTART: ignore_this_directory\hello_world.txt---
This is from the author: "He```llo world!"`
---FILEEND---

---FILEEND---

---FILESTART: requirements.txt---
# Py_markdown-directory-snapshot-special - Minimal requirements file

# The primary functionality of this project uses only Python's standard libraries.
# pytest is included here for testing purposes.
pytest>=8.3.4
flask>=3.0.2
streamlit>=1.29.1

---FILEEND---

---FILESTART: main.py---
import sys
import os
from snapshot_generator import generate_markdown_snapshot
from outdir_generator import generate_outdir

def main():
    if len(sys.argv) < 2:
        print("Usage: program <mode> [args...]")
        print("Modes:")
        print("  snapshot <root_path> [ignore_patterns...]")
        print("  outdir <desired_output_dirname> // write the snapshot to the input.md file before running this mode.")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "snapshot":
        if len(sys.argv) < 3:
            print("Usage: program snapshot <root_path> [ignore_patterns...]")
            sys.exit(1)
        root_path = sys.argv[2]
        ignore_list = sys.argv[3:]
        try:
            generate_markdown_snapshot(root_path, ignore_list)
            print("Snapshot created successfully - go to the output.md file to see the results.")
        except Exception as e:
            print("Error:", str(e))
            sys.exit(1)
    
    elif mode == "outdir":
        print("outdir mode selected... initiating outdir processes...")

        if len(sys.argv) < 3:
            print("Usage: program outdir <desired_output_dirname>")
            print("(╯°□°)╯︵ ┻━┻  Please provide an output directory name!")
            sys.exit(1)
        
        dirname = sys.argv[2]
        try:
            generate_outdir(dirname)
            print(f"Output directory created successfully at directory name '{dirname}'")
        except Exception as e:
            print("Error:", str(e))
            sys.exit(1)
    
    else:
        print(f"Unknown mode '{mode}'")
        sys.exit(1)

if __name__ == "__main__":
    main()

---FILEEND---

---FILESTART: .gitattributes---
# Auto detect text files and perform LF normalization
* text=auto

---FILEEND---

---FILESTART: outdir_generator.py---
import os
from pathlib import Path

def generate_outdir(dirname):
    try:
        os.makedirs(dirname, exist_ok=True)
    except Exception as e:
        raise Exception(f"failed to create directory: {str(e)} (ノಠ益ಠ)ノ彡┻━┻")

    try:
        with open("input.md", "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        raise Exception(f"couldn't read input.md - did you forget to create it? ¯\\_(ツ)_/¯ : {str(e)}")

    # Split content by file markers
    file_blocks = content.split("---FILESTART: ")

    for block in file_blocks[1:]:  # Skip the first empty block
        try:
            # Split into filename and content
            filename, content = block.split("---\n", 1)
            filename = filename.strip()
            
            # Extract content up to FILEEND marker
            content = content.split("---FILEEND---")[0]

            full_path = os.path.join(dirname, filename)
            parent_dir = os.path.dirname(full_path)

            # Create parent directories if they don't exist
            os.makedirs(parent_dir, exist_ok=True)

            # Write the file
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            raise Exception(f"failed to process file {filename}: {str(e)} (╯°□°）╯︵ ┻━┻")
---FILEEND---

---FILESTART: LICENSE---
Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

---FILEEND---

---FILESTART: output.md---

---FILEEND---

---FILESTART: .gitignore---
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
venv
# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/#use-with-ide
.pdm.toml

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

---FILEEND---

---FILESTART: README.md---
# Py_markdown-directory-snapshot-special

Description: Snapshot a directory & save non-excluded results of snapshot in an output.md file | Create a directory from the snapshot in an input.md file

# How to use

First, ensure you have [installed Python](https://www.python.org/downloads/).

In your terminal, navigate to the directory where you want to apply this project, and type the following commands:

```bash
git clone https://github.com/gooddavvy/Py_markdown-directory-snapshot-special
pip install -r requirements.txt
```

Be sure to replace `your-module-name` with your actual module name.

## Creating a Snapshot 📸

To create a snapshot of your directory:

```bash
python main.py snapshot [your_absolute_path] [ignore_patterns...]
```

Replace `your_absolute_path` with the absolute path to the directory you want to snapshot, and `ignore_patterns` with the absolute paths of the files/directories you want to ignore.

An `output.md` file will be created at the root level of this project, containing a snapshot of non-ignored files and their contents.

## Recreating from a Snapshot 🎨

To recreate a directory structure from a snapshot:

1. First, ensure you have an `input.md` file at the root level of the project. This file should follow the format:

````markdown
### path/to/your/file.ext

```content
Your file contents here
```
````

### another/file.ext

```content
More file contents
```

````

2. Then run:
```bash
python main.py outdir [desired_output_dirname]
```

Replace `desired_output_dirname` with the name of the directory you want to create. The program will:

- Create the directory and all necessary subdirectories
- Generate all files with their contents as specified in `input.md` 🎯

Please let me know (in the [Issues Section](https://github.com/gooddavvy/Py_markdown-directory-snapshot-special/issues)) if you encounter any issues during setup or usage.
````

---FILEEND---

---FILESTART: ui.py---
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
        checkbox_key = full_path
        checkbox_keys.append(checkbox_key)
        # Default value: if the entry name is one of the defaults, uncheck it (ignore it)
        default_value = False if entry in DEFAULT_IGNORED_NAMES else True
        indent_str = "&nbsp;" * 4 * indent  # for visual indentation in the label
        label = f"{indent_str}{entry}/" if os.path.isdir(full_path) else f"{indent_str}{entry}"
        checked = st.sidebar.checkbox(label, value=default_value, key=checkbox_key)
        if not checked:
            ignored_paths.append(os.path.abspath(full_path))
        if os.path.isdir(full_path):
            with st.sidebar.expander(f"{indent_str}Contents of {entry}"):
                child_ignored = display_directory_tree(full_path, indent=indent+1, sort_files=sort_files)
                ignored_paths.extend(child_ignored)
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

# Updated: Use full-width buttons by not placing them in columns.
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

---FILEEND---

---FILESTART: snapshot_generator.py---
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

def generate_markdown_snapshot(root_path, ignore_list, max_workers=8):
    # Convert root_path to absolute path
    root_path = Path(root_path).resolve()

    # Prepare the ignore list with absolute paths
    normalized_ignore_set = set()
    for ignore in ignore_list:
        ignore_path = Path(ignore).resolve() if Path(ignore).is_absolute() else (root_path / ignore).resolve()
        normalized_ignore_set.add(ignore_path)

    # Automatically exclude the .git folder by appending its absolute path
    git_ignore = (root_path / ".git").resolve()
    node_modules_ignore = (root_path / "node_modules").resolve()
    py_cache_ignore = (root_path / "__pycache__").resolve()
    venv_ignore = (root_path / "venv").resolve()
    dist_ignore = (root_path / "dist").resolve()
    build_ignore = (root_path / "build").resolve()
    package_lock_ignore = (root_path / "package-lock.json").resolve()
    normalized_ignore_set.update([
        git_ignore,
        node_modules_ignore,
        py_cache_ignore,
        venv_ignore,
        dist_ignore,
        build_ignore,
    ])

    def should_ignore(path):
        for ignore in normalized_ignore_set:
            try:
                path.relative_to(ignore)
                return True
            except ValueError:
                continue
        return False

    def process_file(file_path):
        try:
            with file_path.open('r', encoding='utf-8') as f:
                content = f.read()
            rel_path = file_path.relative_to(root_path)
            return f"---FILESTART: {rel_path}---\n{content}\n---FILEEND---\n\n"
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")
            return ""

    # Collect all files to process
    files_to_process = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        current_dir = Path(dirpath)
        rel_dir = current_dir.relative_to(root_path)

        # Modify dirnames in-place to skip ignored directories
        dirnames[:] = [d for d in dirnames if not should_ignore(current_dir / d)]

        for filename in filenames:
            file_path = current_dir / filename
            if not should_ignore(file_path):
                files_to_process.append(file_path)

    # Write to output.md using multithreading for reading files
    with open("output.md", "w", encoding="utf-8") as output_file:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {executor.submit(process_file, file_path): file_path for file_path in files_to_process}
            for future in as_completed(future_to_file):
                result = future.result()
                if result:
                    output_file.write(result)
---FILEEND---

---FILESTART: test_directory\ignore_this_directory\hello_world.txt---
This is from the author: "Hello world!"
---FILEEND---

---FILESTART: test_directory\hello_world.js---
console.log("This is from the author:")
console.log("Hello world!")
---FILEEND---

---FILESTART: test_directory\accept_this_directory\greetings.txt---
Leoooo!!!! Wuzzupp!!!
---FILEEND---

---FILESTART: test_directory\accept_this_directory\ignore_this_thing.txt---
Don't you dare look at my contained contents!
---FILEEND---

---FILESTART: test_directory\ignore_this_file.txt---
Don't you dare look at my contained contents!
---FILEEND---

