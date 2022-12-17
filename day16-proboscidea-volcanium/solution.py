import re

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


def part1(graph):
    print(graph)

    q = [('AA', 0, 0, set())]
    
    max_pressure = 0

    while q:
        valve_name, pressure, time, open_valves = q[0]
        q = q[1:]
        flow, valves = graph[valve_name]

        if time > 30:
            continue
        if valve_name not in open_valves:
            pressure += flow * (30 - time)
        
        print(time, len(q))

        if pressure > max_pressure:
            max_pressure = pressure

        for vv in valves:
            q.append((vv, pressure, time + 2, open_valves.union({valve_name})))

    return max_pressure


def part1(graph):

    cache = {}

    def check(valve, pressure, time, open_valves):
        key = ':'.join(sorted(open_valves))
        if (valve, time, key) in cache:
            return cache[(valve, time, key)]


        if time >= 30:
            cache[(valve, time, key)] = pressure
            return pressure
        
        flow, valves = graph[valve]

        if flow and valve not in open_valves:
            pressure += flow * (30 - time)
            time = time + 1
        
        results = []
        for vv in valves:
            res = check(vv, pressure, time + 1, open_valves.union({valve}))
            results.append(res)
        retval = max(results) if results else pressure
        cache[(valve, time, key)] = retval
        return retval
    
    res = check('AA', 0, 0, set())
    print(len(cache))
    return res




print('Part 1:', part1(read_input('input')))