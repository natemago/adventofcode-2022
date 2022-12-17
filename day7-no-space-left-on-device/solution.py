class File:

    def __init__(self, name, size):
        self.name = name
        self.size = size
    
    def get_size(self):
        return self.size
    
    def str(self, pref=''):
        return '{} {} (file, size={})'.format(pref, self.name, self.size)


class Dir:

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.abs_path = self.name if not parent else parent.abs_path + '/' + self.name
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
    
    def get_size(self):
        return sum([c.get_size() for c in self.children])
    
    def str(self, pref=''):
        ret = ['{} - {} (dir)'.format(pref, self.name)]

        for c in self.children:
            ret.append('{}{}'.format(pref, c.str(pref+pref)))

        return '\n'.join(ret)


def read_input(inpf):
    dirs = {}
    root = Dir('/')
    dirs[root.abs_path] = root
    cwd = root
    with open(inpf) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            cmd = line.split()
            #print(line)
            if line.startswith('$'):
                # command
                if cmd[1] == 'cd':  # change to dir
                    to_dir = cmd[2]
                    if to_dir == '/':
                        cwd = dirs['/']
                    elif to_dir == '..':
                        cwd = cwd.parent if cwd.parent else cwd
                    else:
                        abs_path = cwd.abs_path + '/' + to_dir
                        next_dir = dirs.get(abs_path)
                        if not next_dir:
                            next_dir = Dir(to_dir, cwd)
                            dirs[next_dir.abs_path] = next_dir
                            cwd.add_child(next_dir)
                        cwd = next_dir
            elif line.startswith('dir'):
                # a directory after ls
                dirname = cmd[1]
                abs_path = cwd.abs_path + '/' + dirname
                next_dir = dirs.get(abs_path)
                if not next_dir:
                    next_dir = Dir(dirname, cwd)
                cwd.add_child(next_dir)
            else:
                # a file with size
                filesize = int(cmd[0])
                filename = cmd[1]
                f = File(filename, filesize)
                cwd.add_child(f)
    
    return root, dirs


def part1(root, dirs):
    total = 0
    for dn, dr in dirs.items():
        size = dr.get_size()
        if size <= 100000:
            total += size
    return total


def part2(root, dirs):
    total = 70000000
    target = 30000000
    used = root.get_size()
    available = total - used
    to_delete = target - available

    print('Used {} of {}.'.format(used, total))
    print('Needs to delete:', to_delete)
    
    for size, d in sorted([(c.get_size(), c) for c in dirs.values()], key=lambda d: d[0]):
        if size >= to_delete:
            return size

    raise Exception('Not found proper sized dir to delete.')


print('Part 1:', part1(*read_input('input')))
print('Part 2:', part2(*read_input('input')))
