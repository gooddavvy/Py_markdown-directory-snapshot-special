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
