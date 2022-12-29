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

directions = {
    '>': (1, 0),
    '^': (0, -1),
    '<': (-1, 0),
    'v': (0, 1),
    (1, 0): '>',
    (0, -1): '^',
    (-1, 0): '<',
    (0, 1): 'v',
}

def get_blizzards(basin):
    blizzards = {}
    for (x, y), c in basin.items():
        if c in '><^v':
            blizzards[(x,y)] = [directions[c]]
    return blizzards

def after_one_minute(basin, width, height, blizzards):
    nbasin = {}
    nblizzards = {}
    
    for (x, y),blzdrs in blizzards.items():
        for dx, dy in blzdrs:
            xx, yy = x+dx, y+dy
            if xx <= 0 or xx >= width-1:
                xx = xx - 1
                xx = xx % (width-2)
                xx = xx + 1
            if yy <= 0 or yy >= height - 1:
                yy = yy - 1
                yy = yy % (height - 2)
                yy = yy + 1
            if nblizzards.get((xx, yy)) is None:
                nblizzards[(xx, yy)] = []
            nblizzards[(xx, yy)].append((dx, dy))
    
    for (x, y), c in basin.items():
        if (x,y) in nblizzards:
            if len(nblizzards[(x,y)]) > 1:
                nbasin[(x, y)] = str(len(nblizzards[(x,y)]))
            else:
                nbasin[(x,y)] = directions[nblizzards[(x,y)][0]]
        elif c in '#SE':
            nbasin[(x, y)] = c
        else:
            if (x, y) not in nbasin:
                nbasin[(x, y)] = '.'
    
    return nbasin, nblizzards

def print_basin(basin, width, height, pos=None):
    for y in range(height):
        for x in range(width):
            if pos and (x, y) == pos:
                if basin[(x, y)] != '.':
                    print('\033[31m' + basin[(x,y)] + '\033[0m', end='')
                else:
                    print('\033[32mO\033[0m', end='')
            else:
                print(basin[(x,y)], end='')
        print()

def get_movable_positions(basin, x, y):
    positions = []
    for dx, dy in ((1, 0), (0, -1), (-1, 0), (0, 1)):
        xx, yy = x+dx, y+dy
        c = basin.get((xx, yy))
        if c and c in '.SE':
            positions.append( (xx, yy) )
    return positions

def move_initial_steps(basin, width, height, blizzards):
    minutes = []
    minutes.append((basin, blizzards))

    r = lcm(width-2, height-2)

    for i in range(r):
        basin, blizzards = after_one_minute(basin, width, height, blizzards)
        minutes.append((basin, blizzards))
    return minutes

def gcd(a, b):
    while b:
        a,b = b, a % b
    return a

def lcm(a, b):
    return (a*b)//gcd(a, b)


def find_way(minutes, width, height, start, end, sminute=0):
    basin, blizzards = minutes[sminute%len(minutes)]
    q = [(start, sminute, 0, [(start, sminute)])]
    seen = set()
    #seen.add((start, 0))

    while q:
        curr, minute, steps, path = q[0]
        q = q[1:]
        if curr == end:
            #print('found it:', minute, steps)
            # for p, m in path:
            #     print(' == At minute {} =='.format(m))
            #     print_basin(minutes[m%len(minutes)][0], width, height, p)
            #     input()

            return minute - sminute

        if (curr, minute%len(minutes)) in seen:
            continue
        seen.add((curr, minute%len(minutes)))

        
        basin, blizzards = minutes[(minute+1) % len(minutes)]

        moves = get_movable_positions(basin, *curr)

        if curr not in blizzards:
            q.append((curr, minute+1, steps, path + [(curr, minute+1)]))

        for pos in moves:
            q.append((pos, minute+1, steps+1, path + [(pos, minute+1)]))
    
    raise Exception('Did not find anything though')

def part1(basin, width, height):
    print('Width:', width)
    print('Height:', height)
    start = (1, 0)
    end = (width-2, height-1)
    basin[start] = 'S'
    basin[end] = 'E'
    blizzards = get_blizzards(basin)
    #print(blizzards)
    print_basin(basin, width, height)

    print('Moving for:', lcm((width-2), (height-2)))

    minutes = move_initial_steps(basin, width, height, blizzards)
    assert basin == minutes[-1][0]
    assert blizzards == minutes[-1][1]
    minutes = minutes[0:-1]

    return find_way(minutes, width, height, start, end)

def part2(basin, width, height):
    print('Width:', width)
    print('Height:', height)
    start = (1, 0)
    end = (width-2, height-1)
    basin[start] = 'S'
    basin[end] = 'E'
    blizzards = get_blizzards(basin)
    #print(blizzards)
    print_basin(basin, width, height)

    print('Moving for:', lcm((width-2), (height-2)))

    minutes = move_initial_steps(basin, width, height, blizzards)
    assert basin == minutes[-1][0]
    assert blizzards == minutes[-1][1]
    minutes = minutes[0:-1]

    m1 = find_way(minutes, width, height, start, end, 0)
    print('Reached end @', m1)
    m2 = find_way(minutes, width, height, end, start, m1)
    print('Got back in ', m2, 'for total minute @', m1+m2)
    m3 = find_way(minutes, width, height, start, end, m1+m2)
    print('Finaly got to the exit in ', m3, 'minutes. Total trip:', m1+m2+m3)

    return m1+m2+m3
    

#print('Part 1:', part1(*read_input('input')))
print('Part 2:', part2(*read_input('input')))