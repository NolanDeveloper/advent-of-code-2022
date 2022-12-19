import pathlib
from dataclasses import dataclass, field


day = int(__file__[-5:-3])
test_input_path = pathlib.Path(f"data/input-{day:02}-test.txt")
real_input_path = pathlib.Path(f"data/input-{day:02}-real.txt")


class TerminalCommand:
    pass


class ChangeDirectoryTarget:
    pass


class Root(ChangeDirectoryTarget):
    pass


class Out(ChangeDirectoryTarget):
    pass


@dataclass
class In(ChangeDirectoryTarget):
    name: str


@dataclass
class ChangeDirectory(TerminalCommand):
    target: ChangeDirectoryTarget


@dataclass
class FileSystemItem:
    name: str


@dataclass
class Directory(FileSystemItem):
    pass


@dataclass
class File(FileSystemItem):
    size: int


@dataclass
class ListFiles(TerminalCommand):
    output: list[FileSystemItem]


def parse(input: str) -> list[TerminalCommand]:
    commands = []
    lines = input.splitlines()
    current_line = 0
    while current_line < len(lines):
        line = lines[current_line]
        current_line += 1
        if line.startswith('$ cd '):
            target_str = line[5:]
            if target_str == '..':
                target = Out()
            elif target_str == '/':
                target = Root()
            else:
                target = In(target_str)
            command = ChangeDirectory(target)
        else:
            assert line.startswith('$ ls')
            items = []
            while current_line < len(lines):
                line = lines[current_line]
                current_line += 1
                if line.startswith('$'):
                    current_line -= 1
                    break
                x, name = line.split()
                if x == 'dir':
                    item = Directory(name)
                else:
                    item = File(name, size=int(x))
                items.append(item)
            command = ListFiles(items)
        commands.append(command)
    return commands


@dataclass
class Node:
    name: str
    size: int = 0
    children: dict[str, 'Node'] = field(default_factory=lambda: {})
    is_directory: bool = True


def add_directory(tree: Node, path: list[str], directory_name: str):
    if not path:
        tree.children[directory_name] = Node(directory_name)
    else:
        add_directory(tree.children[path[0]], path[1:], directory_name)


def add_file(tree: Node, path: list[str], file_name: str, file_size: int):
    if not path:
        tree.children[file_name] = Node(file_name, file_size, is_directory=False)
    else:
        add_file(tree.children[path[0]], path[1:], file_name, file_size)
    tree.size = sum(child.size for child in tree.children.values())


def collect_tree(commands: list[TerminalCommand]):
    tree = Node('/')
    current_directory = []
    for command in commands:
        if isinstance(command, ChangeDirectory):
            target = command.target
            if isinstance(target, Out):
                if current_directory:
                    current_directory.pop()
            elif isinstance(target, Root):
                current_directory = []
            else:
                assert isinstance(target, In)
                add_directory(tree, current_directory, target.name)
                current_directory.append(target.name)
        else:
            assert isinstance(command, ListFiles)
            for file in command.output:
                if isinstance(file, File):
                    add_file(tree, current_directory, file.name, file.size)
    return tree


def dfs(tree: Node, depth=0, debug=False):
    if debug:
        type = 'dir' if tree.is_directory else 'file'
        offset = '  ' * depth
        print(f'{offset}- {tree.name} ({type}, size={tree.size})')
    result = 0
    if tree.is_directory:
        if tree.size < 100000:
            result += tree.size
        for child in tree.children.values():
            result += dfs(child, depth + 1, debug)
    return result


def part1(input_text: str):
    commands = parse(input_text)
    tree = collect_tree(commands)
    return dfs(tree)


def test_part1():
    assert part1(test_input_path.read_text()) == 95437
    assert part1(real_input_path.read_text()) == 1350966


def part2(input_text: str):
    commands = parse(input_text)
    tree = collect_tree(commands)
    total_disc_space = 70000000
    required_free_space = 30000000
    actual_free_space = max(0, total_disc_space - tree.size)
    need_to_free = max(0, required_free_space - actual_free_space)
    best_directory_size = total_disc_space

    def dfs1(tree: Node, depth=0):
        nonlocal best_directory_size
        if not tree.is_directory:
            return
        for child in tree.children.values():
            dfs1(child, depth + 1)
        if tree.size >= need_to_free:
            best_directory_size = min(best_directory_size, tree.size)
    dfs1(tree)
    return best_directory_size


def test_part2():
    assert part2(test_input_path.read_text()) == 24933642
    assert part2(real_input_path.read_text()) == 6296435
