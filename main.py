import os
import re

FIREFOX_THEME_COMMAND = ""

def get_folder_path():
    script_dir = os.path.dirname(os.path(__file__))
    path_file = os.path.join(script_dir, "path.txt")

    if not os.path.isfile(path_file):
        print(f"[ERROR] 'path.txt' not found.")
        exit(1)
    
    with open(path_file, "r", encoding="utf-8") as f:
        path = f.read().strip()
    
    if not os.path.isdir(path):
        print(f"[ERROR] Path in 'path.txt' is invalid. (was: {path})")
        exit(1)
    return path

def normalize_filename(filename):
    if not filename.endswith(".css"):
        filename += ".css"
    return filename

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def firefox_t_command(root_folder, subfolder, filename):
    filename = normalize_filename(filename)
    
    source_path = os.path.join(root_folder, "themes", subfolder, filename)
    target_path = os.path.join(root_folder, "userContent.css")

    if not os.path.isfile(source_path):
        print(f"[ERROR] Source file not found. (was: {source_path})")
        exit(1)
    
    new_block = read_file(source_path).strip()

    comment_pattern = re.escape(subfolder)
    block_pattern = re.compile(
        rf"/\*\s*{comment_pattern}[^\*]*\*/.*?/\*\s*{comment_pattern}[^\*]*\*/",
        re.IGNORECASE | re.DOTALL
    )

    if os.path.isfile(target_path):
        original = read_file(target_path)
        if block_pattern.search(original):
            updated = block_pattern.sub(new_block, original)
            print("[INFO] Existing block replaced.")
        else:
            updated = original.rstrip() + "\n\n" + new_block
            print("[INFO] New block added.")
    else:
        updated = new_block
        print("[INFO] New file created (shouldn't happen tho).")

    write_file(target_path, updated)
    print(f"[OK] '{filename}' has been selected as theme for {subfolder}.")

def parse_command(cmd, root_folder):
    parts = cmd.strip().split()

    if len(parts) == 4 and parts[0].lower() == "firefox" and parts[1].lower() == "t":
        subfolder = parts[2]
        filename = parts[3]
        firefox_t_command(subfolder, filename, root_folder)
    else:
        print("[ERROR] Invalid command")

def main():
    folder_path = get_folder_path()
    print("Commands:\n")
    print("\t" + FIREFOX_THEME_COMMAND)
    print("\t" + "exit")
    while True:
        try:
            command = input("> ")
            if command.strip().lower() in {"exit", "quit"}:
                break
            parse_command(command, folder_path)
        except KeyboardInterrupt:
            print("\nEnded with Ctrl+C")
            break

if __name__ == "__main__":
    main()
