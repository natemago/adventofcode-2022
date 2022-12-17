def read_input(inpf):
    with open(inpf) as f:
        scanned = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            path = [p.strip() for p in line.split('->')]
            points = [(
                int(p.split(',')[0].strip()),
                int(p.split(',')[1].strip()),
            ) for p in path]
            scanned.append(points)
        return scanned

def map_from_scanned(scanned):
    cave = {}
    for path in scanned:
        px, py = path[0]
        cave[(px,py)] = '#'
        for x,y in path[1:]:
            dx,dy = px-x,py-y
            dx,dy = dx/abs(dx) if dx else 0, dy/abs(dy) if dy else 0
            tx,ty = x,y

            while (x,y) != (px,py):
                cave[(x,y)] = '#'
                x,y=x+dx,y+dy
            px,py=tx,ty
    return cave

def print_cave(cave, source=None):
    sx,ex = min([x for x,_ in cave.keys()]),max([x for x,_ in cave.keys()])
    sy,ey = min([y for _,y in cave.keys()]),max([y for _,y in cave.keys()])

    if source:
        sx,ex = min((sx, source[0])), max((ex, source[0]))
        sy,ey = min((sy, source[1])), max((ey, source[1]))

    for y in range(sy,ey+1):
        for x in range(sx, ex+1):
            if (x,y) == source:
                print('+', end='')
                continue
            print(cave.get((x,y), '.'), end='')
        print()


def drop_stone(pos, bottom, cave):
    x,y = pos
    while True:
        # print('  x,y=',(x,y))
        # print_cave(cave, pos)
        # input()
        if cave.get((x, y+1)) is None:
            # move down
            if y+1 > bottom:
                return 'bellow-bottom'
            y = y+1
        else:
            # cannot go down
            # check left first
            if cave.get((x-1, y+1)) is None:
                # drop down left
                if y+1 > bottom:
                    return 'bellow-bottom'
                x,y = x-1, y+1
            elif cave.get((x+1,y+1)) is None:
                # can drop down and to the right
                if y+1 > bottom:
                    return 'bellow-bottom'
                x,y = x+1,y+1
            else:
                # cannot drop anymore
                cave[(x,y)] = 'o'
                return 'settled'

def drop_stone_p2(pos, bottom, cave):
    x,y = pos
    while True:
        # print('  x,y=',(x,y))
        # print_cave(cave, pos)
        # input()
        if cave.get((x, y+1)) is None and y < bottom + 1:
            # move down
            y = y+1
        else:
            # cannot go down
            # check left first
            if cave.get((x-1, y+1)) is None and y < bottom + 1:
                # drop down left
                x,y = x-1, y+1
            elif cave.get((x+1,y+1)) is None and y < bottom + 1:
                # can drop down and to the right
                x,y = x+1,y+1
            else:
                # cannot drop anymore
                cave[(x,y)] = 'o'
                if (x,y) == pos:
                    return 'source-clogged'
                return 'settled'


def part1(scanned):
    cave = map_from_scanned(scanned)
    print_cave(cave, source=(500,0))
    bottom = max([y for _,y in cave.keys()])
    print('Cave bottom is at:', bottom)

    count = 0
    while True:
        res = drop_stone((500, 0), bottom, cave)
        print_cave(cave, (500, 0))
        if res == 'bellow-bottom':
            return count
        count += 1

def part2(scanned):
    cave = map_from_scanned(scanned)
    print_cave(cave, source=(500,0))
    bottom = max([y for _,y in cave.keys()])
    print('Cave bottom is at:', bottom)

    count = 0
    while True:
        res = drop_stone_p2((500, 0), bottom, cave)
        if count % 10 == 0:
            print_cave(cave, (500, 0))
        if res == 'source-clogged':
            return count + 1
        count += 1

#print('Part 1: ', part1(read_input('input')))
print('Part 2: ', part2(read_input('input')))


