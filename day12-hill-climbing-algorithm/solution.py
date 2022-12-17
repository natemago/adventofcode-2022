def read_input(inpf):
    with open(inpf) as f:
        grid = [[ord(c) for c in line.strip()] for line in f if line.strip()]
        start, final = find_positions(grid)

        return grid, start, final


def find_positions(grid):
    start = None
    final = None
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == ord('S'):
                start = (x, y)
            elif c == ord('E'):
                final = (x, y)
    return start, final


def neighbours(grid, x, y):
    h = len(grid)
    w = len(grid[0])
    for xx, yy in ((x+1, y), (x, y-1), (x-1, y), (x, y+1)):
        if xx < 0 or xx >= w or yy < 0 or yy >= h:
            continue
        yield (xx, yy)

def available(grid, x, y):
    curr = grid[y][x]
    for (xx, yy) in neighbours(grid, x, y):
        #print(' .. compare: ', (xx, yy), ' ', grid[yy][xx], ' with ', curr, ' @ ', (x,y))
        if curr not in (ord('S'), ord('E')) and grid[yy][xx] - curr > 1:
            continue
        #print ('yield ', (xx, yy))
        yield (xx, yy)


def part1(grid, start, stop):
    #print(start, stop)
    # BSF start -> stop
    q = [(start, 0)]
    visited = set()

    while q:
        pos, steps = q[0]
        #print('->', pos)
        q = q[1:]
        if pos in visited:
            continue
        visited.add(pos)

        if pos == stop:
            return steps
        
        for xx, yy in available(grid, pos[0], pos[1]):
            #print('go to', (xx, yy))
            q.append(((xx, yy), steps + 1))
    
    raise Exception('No way to final!')

def part2(grid, start, stop):
    result = part1(grid, start, stop)
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == ord('a'):
                try:
                    steps = part1(grid, (x,y), stop)
                    if result is None or steps < result:
                        result = steps
                except:
                    pass
    return result


print('Part 1: ', part1(*read_input('input')))
print('Part 2: ', part2(*read_input('input')))