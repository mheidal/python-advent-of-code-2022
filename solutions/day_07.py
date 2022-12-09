from typing import List


class Directory:
    def __init__(self, name: str, parent):
        self.name = name
        self.files = []
        self.sub_directories = []
        self.parent = parent

    def ls(self, output: List[str]):
        for line in output:
            kind, name = line.split(" ")
            if kind == "dir":
                self.sub_directories.append(Directory(name=name, parent=self))
            else:
                self.files.append(File(name=name, size=int(kind)))

    def get_size(self) -> int:
        return sum(file.size for file in self.files) + sum(
            sub_dir.get_size() for sub_dir in self.sub_directories
        )


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


def cd(current_directory: Directory, target_directory: str, root_directory: Directory):
    if target_directory == "..":
        return current_directory.parent
    elif target_directory == "/":
        return root_directory
    return next(
        directory
        for directory in current_directory.sub_directories
        if directory.name == target_directory
    )


def get_all_directories(root: Directory) -> List[int]:
    dirs = []

    def add_subdirs(directory: Directory):
        dirs.append(directory.get_size())
        dirs.extend(
            subdir.get_size()
            for subdir in directory.sub_directories
            if len(directory.sub_directories) == 0
        )
        for subdir in directory.sub_directories:
            add_subdirs(subdir)

    add_subdirs(root)
    return dirs


def get_file_tree():
    root = Directory(name="/", parent=None)
    current_directory: Directory = None
    with open(f"../inputs/day_07.txt", "r") as input_file:
        command_blocks = input_file.read().split("$ ")
        for block in command_blocks[1:]:
            block = block.strip()
            command = block.split("\n")[0]
            output = block.split("\n")[1:]
            if command.split(" ")[0] == "cd":
                current_directory = cd(current_directory, command.split(" ")[1], root)
            elif command == "ls":
                current_directory.ls(output)

    return root


def part_1():
    root = get_file_tree()
    good_sizes_to_cut = 0
    all_dirs = get_all_directories(root)
    for size in all_dirs:
        if size <= 100000:
            good_sizes_to_cut += size
    print(good_sizes_to_cut)


def part_2():
    mem_size = 70000000
    update_size = 30000000
    root = get_file_tree()
    free_space = mem_size - root.get_size()
    all_dirs = get_all_directories(root)
    print(sorted([size for size in all_dirs if size >= update_size - free_space])[0])


if __name__ == "__main__":
    part_1()
    part_2()
