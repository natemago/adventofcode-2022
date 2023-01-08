import re
from functools import cache
from collections import deque
from itertools import combinations

def read_input(inpf):
    with open(inpf) as f:
        graph = {}
        for line in f:
            m = re.match(r'Valve (?P<valve>\w+) has flow rate=(?P<rate>\d+); tunnels? leads? to valves? (?P<valves>.+)', line)
            if not m:
                raise Exception('Wrong regex for line: %s' % line)
            valve = m.group('valve')
            rate = int(m.group('rate'))
            valves = [v.strip() for v in m.group('valves').split(',')]
            graph[valve] = (rate, valves)
        return graph


class V:

    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
        self.edges = []
    
    def __str__(self):
        return '{}_{}'.format(self.name, self.rate)
    
    def __repr__(self):
        return self.__str__()

class E:

    def __init__(self, s, t, cost=1):
        self.s = s
        self.t = t
        self.cost = cost


class G:

    def __init__(self):
        self.vertices = {}
        self.edges = {}
    
    def vertex(self, name):
        v = self.vertices.get(name)
        if not v:
            raise Exception('No vertex: {}'.format(name))
        return v
    
    def add_edge(self, s, t, cost=1):
        key = (s, t)
        if key in self.edges:
            raise Exception('Edge already exists {}->{}'.format(s, t))
        e = E(s, t, cost)
        self.edges[(s, t)] = e
        s.edges.append(e)

    
    def to_dot(self):
        r = ['digraph {']

        for s, vertex in self.vertices.items():
            for e in vertex.edges:
                r.append('{}_{} -> {}_{} [label="{}"]'.format(e.s.name, e.s.rate, e.t.name, e.t.rate, e.cost))
        r.append('}')
        return '\n'.join(r)

def to_graph(valves):
    g = G()
    for valve, (rate, neighbours) in valves.items():
        v = V(valve, rate)
        g.vertices[valve] = v
    for valve, (rate, neighbours) in valves.items():
        v = g.vertex(valve)
        for t in neighbours:
            t = g.vertex(t)
            g.add_edge(v, t)
    return g

def get_neighbours(g, s):
    result = []

    seen = {s}
    q = []
    for e in s.edges:
        q.append((e.t, 1))
    
    while q:
        curr, cost = q[0]
        q = q[1:]
        if curr in seen:
            continue
        seen.add(curr)
        if curr.rate > 0 or curr.name == 'AA':
            result.append((curr, cost))
            continue
        for e in curr.edges:
            q.append((e.t, cost+1))    

    return result

def smaller_graph(g):
    rg = G()
    for valve, v in g.vertices.items():
        if v.name == 'AA' or v.rate > 0:
            vv = V(v.name, v.rate)
            rg.vertices[vv.name] = vv
    for _, v in rg.vertices.items():
        for nv, cost in get_neighbours(g, g.vertex(v.name)):
            rg.add_edge(v, rg.vertex(nv.name), cost)

    return rg


def find_best(curr, open_valves, time, total_to_open, path):
    if time >= 30:
        return 0
    released = 0
    results = []
    if curr.rate > 0:
        if curr not in open_valves:
            open_released = (30 - time - 1) * curr.rate
            if total_to_open - len(open_valves) <= 1:
                results.append(open_released)

            else:
                for e in curr.edges:
                    r = open_released + find_best(e.t, open_valves.union({curr}), time+2, total_to_open, path)
                    results.append(r)
    
    for e in curr.edges:
        r = released + find_best(e.t, open_valves, time+1, total_to_open, path)
        results.append(r)
    
    return max(results) if results else 0

def dijkstra(graph, start):
    visited = set()
    distance = {
        start: 0
    }

    q = [start]

    while q:
        q.sort(key=lambda n: distance.get(n, 2**32))
        node = q[0]
        q = q[1:]

        if node in visited:
            continue
        visited.add(node)

        curr_cost = distance[node]
        for e in node.edges:
            v = e.t
            vcost = curr_cost + e.cost
            if vcost < distance.get(v, 2**32):
                distance[v] = vcost
            q.append(v)
        
    return distance


def generate_distances_table(graph):
    table = {}
    for _, v in graph.vertices.items():
        distances = dijkstra(graph, v)
        table[v] = distances

    return table

def find_best(start, table):

    @cache
    def _best(time, curr_valve, open_valves):
        if time >= 30:
            return 0
        pressure = (30-time) * curr_valve.rate
        best = pressure
        for v, cost in table[curr_valve].items():
            if v in open_valves:
                continue
            curr_open = tuple(sorted(set(open_valves).union({v}), key=lambda n: n.name))
            curr = _best(time + cost + 1, v, curr_open)
            if curr + pressure > best:
                best = curr + pressure
        return best
    
    return _best(0, start, tuple())


def find_best2(graph, start, table):

    q = deque()
    q.append((start, 0, 0, {start}))
    released = {}

    it = 0
    while q:
        it += 1
        v, time, pressure, open_valves = q.popleft()
        pressure += (26-time) * v.rate

        open_valves = open_valves.union({v})
        fz = frozenset(open_valves)
        released[fz] = max(released.get(fz, 0), pressure)

        for vv, cost in table[v].items():
            if vv in open_valves:
                continue
            if time+1+cost > 26:
                continue
            q.append((vv, time+1+cost, pressure, open_valves))

    ignore = {start}
    max_released = 0
    for s1, p1 in released.items():
        for s2, p2 in released.items():
            if not s1.intersection(s2) != ignore:
                max_released = max(max_released, p1+p2)
    return max_released

def part1(graph):
    graph = to_graph(graph)
    graph = smaller_graph(graph)
    table = generate_distances_table(graph)

    return find_best(graph.vertex('AA'), table)

def part2(graph):
    graph = to_graph(graph)
    graph = smaller_graph(graph)

    table = generate_distances_table(graph)

    return find_best2(graph, graph.vertex('AA'), table)


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))