def read_input(inpf):
    with open(inpf) as f:
        return [(l.split()[0], int(l.split()[1])) for l in f if l.strip()]


directions = {
    'R': (1, 0),
    'U': (0, 1),
    'L': (-1, 0),
    'D': (0, -1)
}


def move(step, pos):
    d, value = step
    dx,dy = directions[d]
    x,y = pos

    x,y=(x+dx*value, y+dy*value)
    
    return (x,y)


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance(self, to_point):
        tx, ty = to_point.x, to_point.y
        return abs(tx-self.x) + abs(ty-self.y)
    
    def no_tension(self, to_point):
        x, y = self.x, self.y
        target = (to_point.x, to_point.y)
        no_tension = (
            (x-1, y-1), (x, y-1), (x+1, y-1),
            (x-1, y),   (x,y),    (x+1, y),
            (x-1, y+1), (x, y+1), (x+1, y+1),
        )
        return target in no_tension
    
    def move_towards(self, tx, ty):
        dx, dy = tx - self.x, ty - self.y
        dx, dy = dx//abs(dx) if dx else 0, dy//abs(dy) if dy else 0
        x,y = self.x + dx, self.y + dy
        if (self.x, self.y) == (x,y):
            return False
        self.x = x
        self.y = y
        return True
    
    def move_to_node(self, n):
        if self.no_tension(n):
            return False
        return self.move_towards(n.x, n.y)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)
    
    def __repr__(self):
        return self.__str__()


def print_wr(visited, path, rope):

    def in_rope(x,y):
        for i, p in enumerate(rope):
            if (x,y) == (p.x, p.y):
                return str(i)
        return None

    for y in range(-20,20): #range(ey-sy):
        for x in range(-50,50): #range(ex-sx):
            if in_rope(x, y):
                print(in_rope(x,y), end='')
            elif (x,y) == (0,0):
                print('s', end='')
            elif (x,y) in visited:
                print('#', end='')
            else:
                print('.', end='')
        print()

def solve(steps, rl=2):
    visited = {(0,0)}
    rope = [Point(0,0) for _ in range(rl)]

    for step in steps:
        h = rope[0]
        tx, ty = move(step, (h.x, h.y))
        while True:
            if not h.move_towards(tx, ty):
                break
            prev = h
            for i,p in enumerate(rope[1:]):
                moved = p.move_to_node(prev)
                prev = p
            visited.add((p.x, p.y)) # add the last position, since we're only moving 1 step at a time...
    print_wr(visited, [], rope)
    return len(visited)


print('Part 1: ', solve(read_input('input'), rl=2))
print()
print('Part 2: ', solve(read_input('input'), rl=10))