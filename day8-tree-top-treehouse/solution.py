b = '    ./░▒▓█'

def read_input(inpf):
    trees = []
    with open(inpf) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            trees.append([int(c) for c in line])
    return trees


def part1(trees):
    visible = [[0 for _ in row] for row in trees]

    ty = len(trees)
    tx = len(trees[0])

    def mark_visible(x, y, dx, dy):
        m = -1
        xx, yy = x, y
        while True:
            if xx < 0 or xx >= tx or yy < 0 or yy >= ty:
                break
            c = trees[yy][xx]
            if c > m:
                visible[yy][xx] = 1
                m = c
            xx, yy = xx + dx, yy + dy
    
    for i in range(ty):
        mark_visible(0, i, 1, 0)
        mark_visible(tx-1, i, -1, 0)
    
    for i in range(tx):
        mark_visible(i, 0, 0, 1)
        mark_visible(i, ty-1, 0, -1)

    return sum([sum(row) for row in visible])


def part2(trees):
    ty = len(trees)
    tx = len(trees[0])

    def score(x, y, dx, dy):
        xx, yy = x, y
        value = 0
        while True:
            xx, yy = xx+dx, yy+dy
            if xx < 0 or xx >= tx or yy < 0 or yy >= ty:
                break

            if trees[y][x] <= trees[yy][xx]:
                value += 1
                break
            value += 1
        return value
    
    def scenic_score(x, y):
        return score(x, y, 0, 1) * score(x, y, 0, -1) * score(x, y, 1, 0) *score(x, y, -1, 0)

    result = -1
    for x in range(tx):
        for y in range(ty):
            if scenic_score(x, y) >= result:
                result = scenic_score(x, y)
    
    return result

print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))
