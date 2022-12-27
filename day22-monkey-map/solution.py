def read_input(inpf):
    with open(inpf) as f:
        wmap = {}
        instructions = None
        consume_instructions = False
        for y, line in enumerate(f.readlines()):
            if not line.strip():
                consume_instructions = True
                continue
            if consume_instructions:
                instructions = line.strip()
                continue
            for x, c in enumerate(line.rstrip()):
                if c != ' ':
                    wmap[(x,y)] = c
        return wmap, instructions

def parse_instructions(instructions):
    res = []
    buff = ''
    for i, c in enumerate(instructions):
        if c in 'RL':
            if buff:
                res.append(('mv', int(buff)))
            res.append(('rot', DIRECTIONS[c]))
            buff = ''
        else:
            buff += c
    if buff:
        res.append(('mv', int(buff)))
    return res

def rotate_90_deg(x, y):
    return -y, x

def rotate_270_deg(x, y):
    return y, -x

def rotate_180_deg(x, y):
    return -x, -y

DIRECTIONS = {
    'R': rotate_90_deg,
    'L': rotate_270_deg,
    'F': lambda x, y: (x, y),
}

DIRECTIONS_MAPPING = {
    (1,0): 0,   # right
    (0, -1): 3, # up 
    (-1, 0): 2, # left
    (0, 1): 1,  # down
}

DIRECTIONS_PATH = {
    (1,0): '>',   # right
    (0, -1): '^', # up 
    (-1, 0): '<', # left
    (0, 1): 'V',  # down
}


def move(wmap, pos, direction, stitched):
    x,y = pos
    dx, dy = direction

    xx, yy = x+dx, y+dy
    if wmap.get((xx, yy)):
        return wmap[(xx, yy)], (xx, yy)

    if (pos, direction) in stitched:
        xx, yy = stitched[(pos, direction)]
        return wmap[(xx, yy)], (xx, yy)
    
    rdx, rdy = rotate_180_deg(dx, dy)
    x, y = pos
    while True:
        xx, yy = x+rdx, y+rdy
        if (xx,yy) not in wmap:
            break
        x,y=xx,yy
    # stich it
    stitched[(pos, direction)] = (x,y)
    # reverse stich it as well
    stitched[((x,y), (rdx, rdy))] = pos
    return wmap[(x,y)], (x,y)

def find_start_point(wmap):
    y = min([n for _,n in wmap.keys()])
    x = min([xx for xx, yy in wmap.keys() if yy == y])
    return (x,y)

def print_wmap(wmap, path):
    sx, sy = min([x for x,_ in wmap.keys()]), min([y for _,y in wmap.keys()])
    ex, ey = max([x for x,_ in wmap.keys()]), max([y for _,y in wmap.keys()])
    for y in range(sy, ey+1):
        for x in range(sx, ex +1):
            c = wmap.get((x,y))
            if (x,y) in path:
                print(DIRECTIONS_PATH[path[(x,y)]], end='')
            else:
                print(c if c else ' ', end='')
        print()

class Node:

    def __init__(self, pos, value):
        self.pos = pos
        self.value = value
        self.edges = [None for _ in range(4)]
    
    def forward(self, from_node):
        idx = self.edges.index(from_node)
        idx = (idx+2) % 4
        return self.edges[idx]
    
    def left(self, from_node):
        idx = self.edges.index(from_node)
        # by convention, left is -1 of where we came from
        idx = (idx-1) % 4
        return self.edges[idx]
    
    def right(self, from_node):
        idx = self.edges.index(from_node)
        # by convention, left is +1 of where we came from
        idx = (idx+1) % 4
        return self.edges[idx]
    
    def add_forward(self, from_node, node):
        idx = self.edges.index(from_node)
        idx = (idx+2) % 4
        self.edges[idx] = node
    
    def add_left(self, from_node, node):
        idx = self.edges.index(from_node)
        idx = (idx-1) % 4
        self.edges[idx] = node
    
    def add_right(self, from_node, node):
        idx = self.edges.index(from_node)
        idx = (idx+1) % 4
        self.edges[idx] = node
    
    def to_right(self, towards):
        idx = self.edges.index(towards)
        idx = (idx - 1) % 4
        return self.edges[idx]
    
    def to_left(self, towards):
        idx = self.edges.index(towards)
        idx = (idx + 1) % 4
        return self.edges[idx]

    def can_stitch(self):
        right, up, left, down = self.edges
        if not (right and up and left and down):
            return False
        
        '''
         X | U |
        ---+---+---
         L | C | R
        ---+---+---
           | D |
        '''
        if up.left(self) is None and left.right(self) is None:
            return [(up, 'add_left'), (left, 'add_right')]
        
        '''
           | U | X
        ---+---+---
         L | C | R
        ---+---+---
           | D |
        '''
        if up.right(self) is None and right.left(self) is None:
            return [(up, 'add_right'), (right, 'add_left')]
        
        '''
           | U | 
        ---+---+---
         L | C | R
        ---+---+---
         X | D |
        '''
        if left.left(self) is None and down.right(self) is None:
            return [(left, 'add_left'), (down, 'add_right')]
        
        '''
           | U | 
        ---+---+---
         L | C | R
        ---+---+---
           | D | X
        '''
        if right.right(self) is None and down.left(self) is None:
            return [(right, 'add_right'), (down, 'add_left')]
        return None
    
    def __repr__(self):
        return self.value
    
    def __str__(self):
        return self.__repr__()

def measure_on_line(wmap, x,y, dx,dy):
    l = 0
    found = False
    while True:
        if (x,y) not in wmap:
            if found:
                break
            x,y = x+dx, y+dy
            continue
        c = wmap[(x,y)]
        if c:
            found = True
            l+=1
        x,y = x+dx, y+dy

    return l

def measure_cube_edge(wmap):
    sx, sy = min([x for x,_ in wmap.keys()]), min([y for _,y in wmap.keys()])
    ex, ey = max([x for x,_ in wmap.keys()]), max([y for _,y in wmap.keys()])
    results = []
    for x in range(sx, ex+1):
        results.append(measure_on_line(wmap, x, sy, 0, 1))
    for y in range(sy, ey+1):
        results.append(measure_on_line(wmap, sx, y, 1, 0))
    
    return min(results)


def to_cube(wmap):
    x,y = find_start_point(wmap)
    root = Node((x,y), wmap[(x,y)])
    # edges is [right, up, left, down]

    nodes = {(x,y): root}
    q = [root]
    seen = set()

    while q:
        node = q[0]
        q = q[1:]
        if node.pos in seen:
            continue
        seen.add(node.pos)
        # print('====')
        # print('Looking at: ', node.value)
        for dx,dy,idx in ((1, 0, 0), (0, -1, 1), (-1, 0, 2), (0, 1, 3)):
            x,y = node.pos
            x,y = x+dx, y+dy
            c = wmap.get((x,y))
            if c:
                nn = nodes.get((x,y))
                if not nn:
                    nn = Node((x,y), c)
                #print(' nn=', nn.value)
                node.edges[idx] = nn
                #print(node.value, '->', nn.value, '@', idx)
                nn.edges[(idx+2)%4] = node
                #print(nn.value, '->', node.value, '@', (idx+2)%4)
                
                nodes[(x,y)] = nn
                
                q.append(nn)
    return root, nodes

def find_to_stitch(nodes):
    for _, node in nodes.items():
        if node.can_stitch():
            yield node

def stich(cube, nodes, wmap):
    edge_len = measure_cube_edge(wmap)

    while True:
        sns = list(find_to_stitch(nodes))
        if not sns:
            print('Cube stitched together.')
            break
        for n in sns:
            if not n.can_stitch():
                continue
            print('Stitching:', n, '->', n.can_stitch())
            a, b = n.can_stitch()
            a, fna = a
            b, fnb = b
            pa = n
            pb = n
            for _ in range(edge_len):
                # print('a=', a, a.edges, 'fn=', fna)
                # print('b=', b, b.edges, 'fn=', fnb)
                getattr(a, fna)(pa, b)
                getattr(b, fnb)(pb, a)

                # print('a`=', a, a.edges, 'fn=', fna)
                # print('b`=', b, b.edges, 'fn=', fnb)

                na = a.forward(pa)
                nb = b.forward(pb)
                pa, pb = a, b
                a, b = na, nb
        # print('---------------------------')
        # for _, node in nodes.items():
        #     print('{} {}'.format(node, node.edges))
        # print('---------------------------')

def part1(wmap, instructions):
    instructions = parse_instructions(instructions)
    path = {}

    stitched = {}
    x, y = find_start_point(wmap)
    direction = (1, 0)  # facing right
    path[(x,y)] = direction

    for instr, op in instructions:
        if instr == 'mv':
            for i in range(op):
                value, pos = move(wmap, (x,y), direction, stitched)
                if value == '#':
                    # we've hit a wall
                    break
                x, y = pos
                path[(x,y)] = direction
        else:
            direction = op(*direction)
    return (y+1)*1000 + (x+1)*4 + DIRECTIONS_MAPPING[direction]


def part2(wmap, instructions):
    instructions = parse_instructions(instructions)
    print('Cube edge:', measure_cube_edge(wmap))
    cube, nodes = to_cube(wmap)
    stich(cube, nodes, wmap)

    curr = cube
    towards = cube.edges[0]
    
    path = {curr.pos: (1,0)}
    directions = {  # absolute directions
        0: (1, 0),
        1: (0, -1),
        2: (-1, 0),
        3: (0, 1),
    }

    for instr, op in instructions:
        if instr == 'mv':
            for i in range(op):
                if towards.value == '#':
                    # hitting a wall
                    break
                n = towards.forward(curr)
                path[curr.pos] = directions[curr.edges.index(towards)]
                curr = towards
                towards = n
            path[curr.pos] = directions[curr.edges.index(towards)]
        else:
            if op == rotate_90_deg:  # RIGHT
                towards = curr.to_right(towards)
            else:
                towards = curr.to_left(towards)
    path[curr.pos] = directions[curr.edges.index(towards)]
    print_wmap(wmap, path)
    
    x, y = curr.pos
    facing = {
        0: 0,
        1: 3,
        2: 2,
        3: 1,
    }
    return (y+1)*1000 + (x+1)*4 + facing[curr.edges.index(towards)]


print('Part 1:', part1(*read_input('input')))
print('Part 2:', part2(*read_input('input')))