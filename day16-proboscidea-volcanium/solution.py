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


class V:

    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
        self.edges = []
    

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
        edge = self.edges.get(key)
        if edge:
            if cost < edge.cost:
                # remove this edge
                self.remove_edge(edge)
                edge = E(s, t, cost)
            else:
                # don't add it
                return edge
        else:
            edge = E(s, t, cost)
        
        s.edges.append(edge)
        self.edges[key] = edge
        return edge

    def remove_edge(self, edge):
        key = (edge.s, edge.t)
        del self.edges[key]
        edge.s.edges.remove(edge)
    
    def remove_vertex(self, v):
        del self.vertices[v.name]
        for e in v.edges:
            self.remove_edge(e)
        # find incoming
        for e in self.get_incoming_edges(v):
            self.remove_edge(e)
    
    def get_incoming_edges(self, v):
        res = []
        for _, e in self.edges.items():
            if e.t == v:
                res.append(e)
        return res
    
    def to_dot(self):
        r = ['digraph {']

        for s, vertex in self.vertices.items():
            for e in vertex.edges:
                r.append('{}_{} -> {}_{} [label="{}"]'.format(e.s.name, e.s.rate, e.t.name, e.t.rate, e.cost))
        r.append('}')
        return '\n'.join(r)

def build_graph(graph):
    g = G()

    for valve, vd in graph.items():
        v = V(valve, vd[0])
        g.vertices[valve] = v

    for valve, vd in graph.items():
        _, valves = vd
        s = g.vertex(valve)
        for tv in valves:
            t = g.vertex(tv)
            g.add_edge(s, t)

    return g


def simplify_graph(g):
    remove_vertices = set()
    for _, v in g.vertices.items():
        if v.rate == 0 and v.name != 'AA':
            remove_vertices.add(v)
    
    for v in remove_vertices:
        inc_edgs = g.get_incoming_edges(v)
        out_edgs = [e for e in v.edges]

        g.remove_vertex(v)

        for ie in inc_edgs:
            s = ie.s
            s_cost = ie.cost
            for oe in out_edgs:
                t = oe.t
                o_cost = oe.cost
                g.add_edge(s, t, s_cost + o_cost)

def part1(graph):
    graph = build_graph(graph)
    #print(graph.to_dot())
    simplify_graph(graph)
    print(graph.to_dot())



part1(read_input('input'))