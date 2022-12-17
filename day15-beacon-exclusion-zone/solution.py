import re

def read_input(inpf):
    with open(inpf) as f:
        sensors = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = re.match(r'Sensor at x=(?P<x>-?\d+), y=(?P<y>-?\d+): closest beacon is at x=(?P<bx>-?\d+), y=(?P<by>-?\d+)', line)
            if not m:
                raise Exception('Wrong line: %s' % line)
            x = int(m.group('x'))
            y = int(m.group('y'))
            bx = int(m.group('bx'))
            by = int(m.group('by'))
            sensors.append(Sensor(x,y,(bx,by)))
        return sensors


def dist(p1, p2):
    # Manhattan distance
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

class Sensor:

    def __init__(self, x,y, beacon):
        self.x = x
        self.y = y
        self.beacon = beacon
        self.range = dist((x,y), beacon)

    def in_range(self, pos):
        return self.range >= dist((self.x, self.y), pos)
    
    def get_node_points(self):
        return (
            ((self.x - self.range - 1, self.y), (1, 1)), # leftmost peak,
            ((self.x + self.range + 1, self.y), (-1, -1)), # right peak,
            ((self.x, self.y + self.range + 1), (1, -1)), # down-most peak,
            ((self.x, self.y - self.range - 1), (-1, 1)), # top-most peak,
        )

    def __str__(self):
        return 'Sensor@({}, {}) with beacon {}'.format(self.x, self.y, self.beacon)
    
    def __repr__(self):
        return self.__str__()


def part1(sensors, row=10):
    beacons = set()
    for s in sensors:
        beacons.add(s.beacon)
    
    midx = sum([s.x for s in sensors])//len(sensors)
    print('Mid X: ', midx)
    print('Beacons:', beacons)

    def _test_points(x, dx):
        x,y = x,row
        count = 0
        while True:
            in_range = False
            for s in sensors:
                if s.in_range((x, y)):
                    in_range = True
                    break
            if in_range:
                if (x, y) not in beacons:
                    print((x,y))
                    count += 1
            else:
                break
            x += dx
        return count
    
    return _test_points(midx+1, 1) + _test_points(midx, -1)


def part2(sensors, rng):
    beacons = set()
    for s in sensors:
        beacons.add(s.beacon)

    for s in sensors:
        print('Examining around sensor ', s)
        points = s.get_node_points()
        for p, direction in points:
            x,y = p
            dx,dy = direction
            for _ in range(s.range):
                if x >= rng[0] and x <= rng[1] and y >= rng[0] and y <= rng[1]:
                    in_range = False
                    for ss in sensors:
                        if ss.in_range((x,y)):
                            in_range = True
                            break
                    if not in_range and (x,y) not in beacons:
                        return x*4000000 + y, (x,y)
                x,y = x+dx, y+dy


#print('Part 1:', part1(read_input('input'), 2000000))
print('Part 2:', part2(read_input('input'), [0, 4000000]))