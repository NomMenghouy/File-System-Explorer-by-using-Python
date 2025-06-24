class Node:
    def __init__(self, name, is_dir, parent=None):
        self.name = name
        self.is_dir = is_dir
        self.parent = parent
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def remove_child(self, name):
        self.children = [child for child in self.children if child.name != name]

    def find_child(self, name):
        for child in self.children:
            if child.name == name:
                return child
        return None

def display_tree(node, indent=0):
    prefix = "[DIR] " if node.is_dir else "[FILE]"
    print("  " * indent + prefix + node.name)
    for child in node.children:
        display_tree(child, indent + 1)

def search_tree(node, target):
    if node.name == target:
        return node
    for child in node.children:
        result = search_tree(child, target)
        if result:
            return result
    return None

def hint():
    print(" Available Commands:")
    print("  mkdir <folder_name>   - Create a folder")
    print("  touch <file_name>     - Create a file")
    print("  ls                    - List current directory")
    print("  cd <folder_name>      - Enter folder")
    print("  cd ..                 - Go back (up one level)")
    print("  rm <name>             - Remove file or empty folder")
    print("  tree                  - Show folder tree")
    print("  search <name>         - Search for item by name")
    print("  help                  - Show this help menu")
    print("  exit                  - Exit the explorer\n")


def main():
    root = Node("root", True)
    current = root

    print("File System Explorer")
    hint()

    while True:
        cmd = input(f"[{current.name}]$ ").strip()
        if cmd == "ls":
            for child in current.children:
                prefix = "[DIR]" if child.is_dir else "[FILE]"
                print(f"{prefix} {child.name}")

        elif cmd.startswith("cd "):
            target = cmd[3:].strip()
            if target == "..":
                if current.parent:
                    current = current.parent
                else:
                    print("Already at root.")
            else:
                next_dir = current.find_child(target)
                if next_dir and next_dir.is_dir:
                    current = next_dir
                else:
                    print("Folder not found.")

        elif cmd.startswith("mkdir "):
            name = cmd[6:].strip()
            if current.find_child(name):
                print("Name already exists.")
            else:
                folder = Node(name, True, current)
                current.add_child(folder)

        elif cmd.startswith("touch "):
            name = cmd[6:].strip()
            if current.find_child(name):
                print("Name already exists.")
            else:
                file = Node(name, False, current)
                current.add_child(file)

        elif cmd.startswith("rm "):
            name = cmd[3:].strip()
            target = current.find_child(name)
            if target:
                current.remove_child(name)
                print(f"{name} deleted.")
            else:
                print("Not found.")

        elif cmd.startswith("search "):
            name = cmd[7:].strip()
            result = search_tree(root, name)
            if result:
                path = []
                temp = result
                while temp:
                    path.insert(0, temp.name)
                    temp = temp.parent
                print("Found at: /" + "/".join(path))
            else:
                print("Not found.")
        elif cmd == "help":
            hint()

        elif cmd == "tree":
            display_tree(root)

        elif cmd == "exit":
            print("Goodbye!")
            break

        else:
            print("Unknown command. Try: ls, cd, mkdir, touch, rm, search, tree, exit")

if __name__ == "__main__":
    main()
