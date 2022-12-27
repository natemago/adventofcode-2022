def read_input(inpf):
    with open(inpf) as f:
        basin = {}
        y = 0
        for line in f:
            line = line.strip()
            if not line:
                continue
            width = len(line)
            for x, c in enumerate(line):
                basin[(x, y)] = c
            y+=1
        return basin, width, y

def get_blizzards(basin):
    blizzards = {}
    directions = {
        '>': (1, 0),
        '^': (0, -1),
        '<': (-1, 0),
        'v': (0, 1),
    }
    for (x, y), c in basin.items():
        if c in '><^v':
            blizzards[(x,y)] = directions[c]
    return blizzards

def part1(basin, width, height):
    print('Width:', width)
    print('Height:', height)
    blizzards = get_blizzards(basin)
    print(blizzards)


print('Part 1:', part1(*read_input('test_input')))