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