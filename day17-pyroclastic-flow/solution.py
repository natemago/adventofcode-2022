def read_input(inpf):
    with open(inpf) as f:
        return f.read().strip()

class Shape:

    def __init__(self, shape, x=0, y=0):
        self.shape = shape
        self.x = x
        self.y = y

        minx,maxx = min([x for x,_ in shape]), max([x for x,_ in shape])
        miny,maxy = min([y for _,y in shape]), max([y for _,y in shape])

        self.width = maxx-minx + 1
        self.height = maxy-miny + 1
    
    def collide(self, world):
        world_max_y = max([y for _,y in world]) if world else self.height + 2
        for x,y in self.shape:
            xx = self.x + x
            yy = self.y + y
            if xx < 0 or xx > 6:
                # hits the walls
                return True
            if (xx,yy) in world:
                # overlaps with another figure
                return True
            if yy > world_max_y:
                # hit the bottom
                return True
        return False
    
    def get_shape(self):
        s = set()
        for x,y in self.shape:
            xx = self.x + x
            yy = self.y + y
            s.add((xx,yy))
        return s


SHAPES = [{
    (0,0), (1,0), (2,0), (3,0)
}, {
           (1,0),
    (0,1), (1,1), (2,1),
           (1,2),
}, {
                  (2, 0),
                  (2, 1),
    (0,2), (1,2), (2, 2) ,
}, {
    (0,0),
    (0,1),
    (0,2),
    (0,3),
}, {
    (0,0), (1,0),
    (0,1), (1,1),
}]

def printw(world, shape):
    max_y = max([
        max([y for _,y in world]) if world else 0,
        max([y for _,y in shape]),
    ])
    for y in range(max_y+1):
        for x in range(0, 7):
            if (x,y) in shape:
                print('@', end='')
            elif (x,y) in world:
                print('#', end='')
            else:
                print('.', end='')
        print()


def shift_world(world, shape):
    miny = min([y for _,y in world]) if world else 0
    dy = (shape.y + shape.height + 3) - miny

    res = set()
    for x,y in world:
        res.add((x, y+dy))
    return res

def get_last_pattern(world, rows):
    world = sorted(world, key=lambda p: p[1])
    res = []
    for x,y in world:
        if y >= rows:
            break
        res.append((x,y))
    return res

def get_last_state(world, rows):
    return ''.join(['{}'.format(p) for p in get_last_pattern(world, rows)])

def get_world_height(world):
    return max([y for _,y in world]) - min([y for _,y in world]) + 1

def simulate(movements, max_shapes_settled=None, world=None, sp=None, i=None):
    sp = sp if sp is not None else 0
    shape = Shape(SHAPES[sp],x=2)
    world = world if world is not None else set()
    shapes_settled_count = 0

    seen = {
        (0, 0, get_last_state(world, 20)): (0, 0), 
    }

    i = i if i is not None else 0
    while True:
        c = movements[i]
        px,py = shape.x, shape.y
        if c == '>':
            shape.x += 1
        else:
            shape.x -= 1
        if shape.collide(world):
            # cannot move left-right
            #print('  cannot move - hits the wall.')
            shape.x = px
        # try to move down
        shape.y += 1
        if shape.collide(world):
            # cannot go down, we must settle here
            shape.y = py
            for p in shape.get_shape():
                world.add(p)
            
            shapes_settled_count += 1
            if max_shapes_settled is not None and shapes_settled_count == max_shapes_settled:
                return world

            sp = (sp+1) % len(SHAPES)
            shape = Shape(SHAPES[sp], x=2)
            world = shift_world(world, shape)

            t = (i+1) % len(movements)
            state = get_last_state(world, 20)
            if (sp, t, state) in seen:
                if max_shapes_settled is None:
                    prev_height, prev_shapes_settled_count = seen[(sp, t, state)]
                    curr_height = get_world_height(world)

                    return (prev_shapes_settled_count, prev_height, shapes_settled_count, curr_height, get_last_pattern(world, 20), sp, t)
                
            seen[(sp, t, state)] = (get_world_height(world), shapes_settled_count)
        
        i = (i+1) % len(movements)
    
    return world


def part1(movements, shps_count):
    world = simulate(movements, shps_count)
    return get_world_height(world)

def part2(movements):
    psc, ph, sc, ch, last_state, sp, t = simulate(movements)
    print('Prev shapes count:', psc)
    print('Prev height:', ph)
    print('Current shapes count:', sc)
    print('Current height:', ch)

    shapes_repeating = sc - psc
    height_repeating = ch - ph
    print('Repeating shapes:', shapes_repeating)
    print('Repeating height:', height_repeating)

    total_rocks = 1000000000000

    repeating = (total_rocks - psc) // shapes_repeating
    up_to = repeating * shapes_repeating + psc
    run_more = total_rocks - up_to
    print('Repeating chunks:', repeating)
    print('Up to:', up_to)
    print('Need to run:', run_more)
    print('Start shape:', sp)
    print('Movement command ptr:', t)

    # Now we have to restart the simulation until we have all rocks fallen
    world = set(last_state)
    world_height_start = get_world_height(world)
    world = simulate(movements, max_shapes_settled=run_more, world=world, sp=sp, i=t)
    world_height_now = get_world_height(world)

    height_calc = ph + repeating*height_repeating
    return height_calc + (world_height_now - world_height_start)


print('Part 1:', part1(read_input('input'), 2022))
print('Part 2:', part2(read_input('input')))