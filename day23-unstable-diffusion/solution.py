def read_input(inpf):
    with open(inpf) as f:
        elves = {}
        y = 0
        for line in f:
            line = line.strip()
            if not line:
                continue
            for x, c in enumerate(line):
                if c == '#':
                    elves[(x, y)] = 1
            y += 1
        return elves


directions = [
    ((-1, -1), (0, -1), (1, -1)), # North
    ((-1,  1), (0,  1), (1,  1)), # South
    ((-1, -1), (-1, 0), (-1, 1)), # West
    ((1, - 1), (1,  0), (1,  1)), # East
]

move_direction = {
    0: (0, -1), # Move north
    1: (0,  1), # Move south
    2: (-1, 0), # Move west
    3: (1,  0), # Move east
}

def elves_in_direction(elves, elf, direction):
    x,y=elf
    for dx, dy in direction:
        if elves.get((x+dx, y+dy)):
            return True
    return False

def get_free_direction(elves, step, x, y):
    for i in range(4):
    #for d, direction in enumerate(directions):
        d = (i+step) % 4
        direction = directions[d]
        if not elves_in_direction(elves, (x,y), direction):
            return d, move_direction[d]

def should_move(elves, step, x,y):
    for i in range(4):
        direction = directions[(i+step) % 4]
        if elves_in_direction(elves, (x,y), direction):
            return True
    return False

def move_elves(elves, step):
    moved_elves = {}
    for elf in elves.keys():
        dd = get_free_direction(elves, step, *elf)
        if should_move(elves, step, *elf) and dd:
            d, delta = dd
            x,y = elf[0] + delta[0], elf[1] + delta[1]
            if moved_elves.get((x,y)) is None:
                moved_elves[(x,y)] = []
            moved_elves[(x,y)].append(elf)
        else:
            # no good position, elf will stay put
            if moved_elves.get(elf) is None:
                moved_elves[elf] = []
            moved_elves[elf].append(elf)
    
    result = {}

    for pos, elves in moved_elves.items():
        if len(elves) > 1:
            for elf in elves:
                result[elf] = 1
        else:
            result[pos] = 1

    return result


def print_elves(elves):
    sx, sy = min([x for x,_ in elves.keys()]), min([y for _,y in elves.keys()])
    ex, ey = max([x for x,_ in elves.keys()]), max([y for _,y in elves.keys()])
    for y in range(sy, ey+1):
        for x in range(sx, ex+1):
            if elves.get((x,y)):
                print('#', end='')
            else:
                print('.', end='')
        print()

def part1(elves):
    print_elves(elves)

    for i in range(10):
        elves = move_elves(elves, i)
    sx, sy = min([x for x,_ in elves.keys()]), min([y for _,y in elves.keys()])
    ex, ey = max([x for x,_ in elves.keys()]), max([y for _,y in elves.keys()])
    print_elves(elves)
    return (ex-sx+1)*(ey-sy+1) - len(elves)

def part2(elves):
    i = 0
    while True:
        moved = move_elves(elves, i)
        i += 1
        if moved == elves:
            break
        elves = moved
    return i

print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))
