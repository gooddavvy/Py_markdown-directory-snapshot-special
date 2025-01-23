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

    sections = content.split("### ")

    for section in sections[1:]:
        parts = section.split("\n```\n", 1)
        if len(parts) != 2:
            continue

        filename = parts[0].strip()
        content = parts[1].split("```")[0]

        full_path = os.path.join(dirname, filename)
        parent_dir = os.path.dirname(full_path)

        try:
            os.makedirs(parent_dir, exist_ok=True)
        except Exception as e:
            raise Exception(f"failed to create directories for {filename}: {str(e)} (ಥ﹏ಥ)")

        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            raise Exception(f"failed to write file {filename}: {str(e)} (╯°□°）╯︵ ┻━┻")