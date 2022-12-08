def read_input(inpf):
    with open(inpf) as f:
        return [[
            (int(line.strip().split(',')[0].split('-')[0]),int(line.strip().split(',')[0].split('-')[1])),
            (int(line.strip().split(',')[1].split('-')[0]),int(line.strip().split(',')[1].split('-')[1])),
        ] for line in f]


def fully_contains(i1, i2):
    if i1[0] <= i2[0] and i1[1] >= i2[1]:
        return True
    return i2[0] <= i1[0] and i2[1] >= i1[1]

def between(x, a, b):
    return a <= x and x <=b

def overlap(i1, i2):
    return between(i1[0], *i2) or between(i1[0], *i2) or between(i2[0], *i1) or between(i2[1], *i1)

def part1(pairs):
    total = 0
    for p0, p1 in pairs:
        if fully_contains(p0, p1):
            total += 1
    return total

def part2(pairs):
    total = 0
    for p0, p1 in pairs:
        if overlap(p0, p1):
            total += 1
    return total



print('Part 1: ', part1(read_input('input')))
print('Part 2: ', part2(read_input('input')))
