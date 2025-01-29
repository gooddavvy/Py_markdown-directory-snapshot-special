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
            return f"### {rel_path}\n```\n{content}\n```\n\n"
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