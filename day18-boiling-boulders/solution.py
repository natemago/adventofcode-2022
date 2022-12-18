def read_input(inpf):
    with open(inpf) as f:
        points = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            x,y,z = line.split(',')
            points.append((
                int(x.strip()),
                int(y.strip()),
                int(z.strip()),
            ))
        return points

def get_adjacent(x,y,z):
    return (
        (x,y+1,z), # up
        (x,y-1,z), # down
        (x-1,y,z), # left
        (x+1,y,z), # right
        (x,y,z+1), # in
        (x,y,z-1), # out
    )

def fill(p, cubes):
    minx, maxx = min([x for x,_,_ in cubes]), max([x for x,_,_ in cubes])
    miny, maxy = min([y for _,y,_ in cubes]), max([y for _,y,_ in cubes])
    minz, maxz = min([z for _,_,z in cubes]), max([z for _,_,z in cubes])

    filled = set()
    q = [p]
    while q:
        p = q[0]
        q = q[1:]

        if p in cubes or p in filled:
            continue
        filled.add(p)

        for x,y,z in get_adjacent(*p):
            if x < minx or x > maxx or y < miny or y > maxy or z < minz or z > maxz:
                # flows off into the water - not an air pocket
                return set()
            q.append((x,y,z))
    
    return filled

def part1(cubes):
    cubes = set(cubes)

    total = 0
    for x,y,z in cubes:
        adjacent = set(get_adjacent(x,y,z))
        covered = len(cubes.intersection(adjacent))
        total += 6 - covered
    
    return total

def part2(cubes):
    cubes = set(cubes)
    minx, maxx = min([x for x,_,_ in cubes]), max([x for x,_,_ in cubes])
    miny, maxy = min([y for _,y,_ in cubes]), max([y for _,y,_ in cubes])
    minz, maxz = min([z for _,_,z in cubes]), max([z for _,_,z in cubes])

    for x in range(minx, maxx+1):
        for y in range(miny, maxy+1):
            for z in range(minz, maxz+1):
                air_pocket = fill((x,y,z), cubes)
                if air_pocket:
                    cubes = cubes.union(air_pocket)
    
    return part1(cubes)


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))