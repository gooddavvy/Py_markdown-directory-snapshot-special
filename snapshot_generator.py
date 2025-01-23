import os
from pathlib import Path

def generate_markdown_snapshot(root_path, ignore_list):
    # Convert root_path to absolute path
    root_path = str(Path(root_path).resolve())
    
    # Convert ignore_list paths to absolute paths relative to root_path
    normalized_ignore_list = []
    for ignore in ignore_list:
        if os.path.isabs(ignore):
            normalized_ignore_list.append(str(Path(ignore).resolve()))
        else:
            normalized_ignore_list.append(str(Path(root_path, ignore).resolve()))

    with open("output.md", "w", encoding="utf-8") as output_file:
        def should_ignore(path):
            # Convert relative path to absolute path using root_path
            abs_path = str(Path(root_path, path).resolve())
            
            for ignore in normalized_ignore_list:
                if abs_path == ignore or str(abs_path).startswith(f"{ignore}{os.sep}"):
                    return True
            return False

        for root, _, files in os.walk(root_path):
            rel_root = os.path.relpath(root, root_path)
            if rel_root != "." and should_ignore(rel_root):
                continue

            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, root_path)
                
                if should_ignore(rel_path):
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    output_file.write(f"### {rel_path}\n```\n{content}\n```\n\n")
                except Exception as e:
                    print(f"Warning: Could not read {file_path}: {str(e)}")