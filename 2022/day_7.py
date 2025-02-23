



class directory:
    total_trash_size = 0
    max_space_available = 70000000
    required_space = 30000000
    max_occupied_space = max_space_available - required_space
    smallest_dir_to_delete = 70000000
    def __init__(self, children = None, files = None, parent = None, name=None):
        self.children = {} if children is None else children
        self.files = [] if files is None else files
        self.parent = parent
        self.size = 0
        self.name = name

    def compute_size(self):
        file_size = sum(file[0] for file in self.files)
        dir_size = 0

        for child_name, dir in self.children.items():
            dir_size += dir.compute_size()
        
        total_size = file_size + dir_size
        self.size = total_size
        #print(f'size of {self.name} is {self.size}')
        if self.size <= 100000:
            directory.total_trash_size += self.size
        return total_size

    def compute_delete_candidate(self, space_occupied):
        for child_name, dir in self.children.items():
            child_size = dir.size

            if space_occupied - child_size < directory.max_occupied_space:
                directory.smallest_dir_to_delete = min(directory.smallest_dir_to_delete, child_size)
            
            dir.compute_delete_candidate(space_occupied)






with open('input_7.txt', 'r') as f:
    commands = []
    for line in f:
        commands.append(line.rstrip())


root = directory(name = '/')
current_dir = root


for command in commands[2:]:
    command = command.split()

    if command[0] == '$':
        if command[1] == 'cd':
            if command[2] == '/':
                current_dir = root
            elif command[2] == '..':
                current_dir = current_dir.parent
            else:
                current_dir = current_dir.children[command[2]]
    elif command[0] == 'dir':
        new_dir = directory(name = command[1], parent = current_dir)
        current_dir.children[new_dir.name] = new_dir
    else:
        file_size, file_name = command
        current_dir.files.append((int(file_size), file_name))

root.compute_size()

print(f'found {directory.total_trash_size} worth of trash')

root.compute_delete_candidate(root.size)

print(f'smallest directory to be deleted is of size {directory.smallest_dir_to_delete}')