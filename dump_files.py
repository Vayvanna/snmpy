import os

def main():
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    output_file_path = os.path.join(parent_dir, "all_contents.txt")

    with open(output_file_path, "w", encoding="utf-8") as output:
        # First, write the folder hierarchy (like ls -R)
        output.write("== Folder Hierarchy (like ls -R) ==\n\n")
        for root, dirs, files in os.walk(current_dir):
            output.write(f"{os.path.relpath(root, current_dir)}/\n")
            for d in dirs:
                output.write(f"  {d}/\n")
            for f in files:
                output.write(f"  {f}\n")
            output.write("\n")

        # Then, write each file's full path and its content
        output.write("\n== File Contents ==\n\n")
        for root, _, files in os.walk(current_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, current_dir)
                output.write(f"\n--- {rel_path} ---\n")
                try:
                    with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                        output.write(f.read())
                except Exception as e:
                    output.write(f"[Error reading file: {e}]")
                output.write("\n")

    print(f"Output written to: {output_file_path}")

if __name__ == "__main__":
    main()
