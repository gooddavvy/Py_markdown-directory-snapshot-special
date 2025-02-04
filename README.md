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

Example:

```bash
python main.py snapshot "C:\Users\davvy\Desktop\test" "C:\Users\davvy\Desktop\test\ignore_this_file.txt" "C:\Users\davvy\Desktop\test\ignore_this_directory"
```

An `output.md` file will be created at the root level of this project, containing a snapshot of non-ignored files and their contents.

**Alternatively, if you want to use our UI, run the following command to launch our Streamlit app (instructions to use it will be shown there):**

```bash
python3 -m streamlit run ui.py --port 5000
```

If you are on a Windows machine and only `py` works for you, run the following command instead:

```bash
py -3 -m streamlit run ui.py --port 5000
```

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
